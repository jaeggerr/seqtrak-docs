// Point 6 — BLE trace: negotiated MTU and raw packets from the SEQTRAK.
//
// Read-only on the MIDI level: this tool subscribes to notifications and never
// writes to the characteristic unless --poke is given. The MTU is learned from
// the connection itself and needs no MIDI traffic at all.
//
//   swift ble_trace.swift [--seconds N] [--poke]
//
// Nothing in seqtrak-apple or seqtrak-lib is imported or modified.

import Foundation
import CoreBluetooth

let MIDI_SERVICE = CBUUID(string: "03B80E5A-EDE8-4B33-A751-6CE34EC4C700")
let MIDI_IO = CBUUID(string: "7772E5DB-3868-4112-A1A9-F2669D106BF3")

func hex(_ b: [UInt8]) -> String { b.map { String(format: "%02X", $0) }.joined(separator: " ") }

var seconds: Double = 60
var scanSeconds: Double = 20
var poke = false
var dumpPath: String? = nil
var args = CommandLine.arguments.dropFirst().makeIterator()
while let a = args.next() {
    switch a {
    case "--seconds": if let v = args.next(), let d = Double(v) { seconds = d }
    case "--scan": if let v = args.next(), let d = Double(v) { scanSeconds = d }
    case "--dump": dumpPath = args.next()
    case "--poke": poke = true
    default: break
    }
}

/// One received packet, kept whole. Nothing is summarised at capture time.
struct Packet {
    let t: Double
    let bytes: [UInt8]
}

final class Trace: NSObject, CBCentralManagerDelegate, CBPeripheralDelegate {
    var central: CBCentralManager!
    var peripheral: CBPeripheral?
    var io: CBCharacteristic?
    var packets: [Packet] = []
    var t0 = Date()
    var connectedAt: Date?
    var finished = false

    func start() {
        central = CBCentralManager(delegate: self, queue: nil)
    }

    func centralManagerDidUpdateState(_ c: CBCentralManager) {
        let names: [CBManagerState: String] = [
            .unknown: "unknown", .resetting: "resetting", .unsupported: "unsupported",
            .unauthorized: "unauthorized — the host app has no Bluetooth permission",
            .poweredOff: "poweredOff", .poweredOn: "poweredOn",
        ]
        print("CBCentralManager state: \(names[c.state] ?? "?")")
        guard c.state == .poweredOn else {
            if c.state == .unauthorized || c.state == .unsupported {
                print("RESULT: cannot scan — \(names[c.state]!)")
                exit(2)
            }
            return
        }
        print("scanning for the MMA MIDI service \(MIDI_SERVICE.uuidString)…")
        c.scanForPeripherals(withServices: [MIDI_SERVICE], options: nil)
        DispatchQueue.main.asyncAfter(deadline: .now() + scanSeconds) {
            if self.peripheral == nil {
                print("RESULT: no peripheral advertising the MIDI service in \(Int(scanSeconds)) s.")
                print("        (Bluetooth MIDI In/Out `00 00 11` must be on, and the")
                print("         machine must be in pairing mode: hold [ALL], press [SWING].)")
                exit(3)
            }
        }
    }

    func centralManager(_ c: CBCentralManager, didDiscover p: CBPeripheral,
                        advertisementData d: [String: Any], rssi: NSNumber) {
        let name = (d[CBAdvertisementDataLocalNameKey] as? String) ?? p.name ?? "(no name)"
        print("discovered \"\(name)\"  rssi \(rssi)  id \(p.identifier)")
        guard name.uppercased().hasPrefix("SEQTRAK") else {
            print("  not a SEQTRAK, ignored"); return
        }
        c.stopScan()
        peripheral = p
        p.delegate = self
        c.connect(p, options: nil)
    }

    func centralManager(_ c: CBCentralManager, didConnect p: CBPeripheral) {
        connectedAt = Date()
        print("connected.")
        // These are the negotiated ATT MTU minus the 3-byte ATT header.
        let woR = p.maximumWriteValueLength(for: .withoutResponse)
        let wR = p.maximumWriteValueLength(for: .withResponse)
        print("")
        print("=== NEGOTIATED WRITE CEILING ===")
        print("maximumWriteValueLength(.withoutResponse) = \(woR) bytes  -> ATT MTU \(woR + 3)")
        print("maximumWriteValueLength(.withResponse)    = \(wR) bytes")
        print("")
        p.discoverServices([MIDI_SERVICE])
    }

    func peripheral(_ p: CBPeripheral, didDiscoverServices error: Error?) {
        guard let s = p.services?.first(where: { $0.uuid == MIDI_SERVICE }) else {
            print("RESULT: MIDI service not present on this peripheral"); exit(4)
        }
        p.discoverCharacteristics([MIDI_IO], for: s)
    }

    func peripheral(_ p: CBPeripheral, didDiscoverCharacteristicsFor s: CBService, error: Error?) {
        guard let c = s.characteristics?.first(where: { $0.uuid == MIDI_IO }) else {
            print("RESULT: MIDI I/O characteristic not present"); exit(5)
        }
        io = c
        var props: [String] = []
        if c.properties.contains(.notify) { props.append("notify") }
        if c.properties.contains(.write) { props.append("write") }
        if c.properties.contains(.writeWithoutResponse) { props.append("writeWithoutResponse") }
        if c.properties.contains(.read) { props.append("read") }
        print("characteristic properties: \(props.joined(separator: ", "))")
        p.setNotifyValue(true, for: c)
        t0 = Date()
        print("subscribed; capturing \(Int(seconds)) s — manipulate the machine now.\n")

        if poke {
            // A Parameter Request is read-only in effect: it asks for the tempo.
            let req: [UInt8] = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C, 0x30, 0x40, 0x76, 0xF7]
            // 13-bit millisecond timestamp. Reduce in Int first: the raw
            // millisecond count is ~1.79e12 and trapping it into UInt16
            // directly is a runtime precondition failure.
            let ms = Int(Date().timeIntervalSince1970 * 1000) & 0x1FFF
            var pkt: [UInt8] = [UInt8(0x80 | (ms >> 7)), UInt8(0x80 | (ms & 0x7F))]
            pkt.append(contentsOf: req)
            let kind: CBCharacteristicWriteType =
                c.properties.contains(.writeWithoutResponse) ? .withoutResponse : .withResponse
            print("poke: writing a tempo Parameter Request, \(pkt.count) bytes: \(hex(pkt))")
            p.writeValue(Data(pkt), for: c, type: kind)
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + seconds) { self.report() }
    }

    func peripheral(_ p: CBPeripheral, didUpdateValueFor c: CBCharacteristic, error: Error?) {
        guard let d = c.value else { return }
        packets.append(Packet(t: Date().timeIntervalSince(t0), bytes: [UInt8](d)))
    }

    func centralManager(_ c: CBCentralManager, didDisconnectPeripheral p: CBPeripheral,
                        error: Error?) {
        print("\n!! disconnected: \(error?.localizedDescription ?? "no error")")
        if !finished { report() }
    }

    // MARK: - analysis

    func report() {
        finished = true
        print("\n" + String(repeating: "=", count: 72))
        print("BLE capture — \(packets.count) notification packets in \(Int(seconds)) s")
        print(String(repeating: "=", count: 72))

        if packets.isEmpty {
            print("""

            No packets. That is NOT evidence that the machine sends nothing:
            check `00 00 11` (Bluetooth MIDI In/Out), `00 00 13` and `00 00 14`
            over USB first, and make sure gestures were actually made.
            """)
            exit(0)
        }

        var maxLen = 0, totalBytes = 0
        var untimestampedF7 = 0, timestampedF7 = 0
        var f7Examples: [String] = []
        var statusCounts: [UInt8: Int] = [:]

        for pk in packets {
            let b = pk.bytes
            maxLen = max(maxLen, b.count)
            totalBytes += b.count
            // index 0 is the BLE header; a timestamp byte also has bit 7 set.
            var i = 1
            while i < b.count {
                if b[i] == 0xF7 {
                    // Inside a SysEx body every data byte is 0x00-0x7F, so a
                    // preceding byte with bit 7 set (and not the BLE header at
                    // index 0) is the interleaved timestamp the MMA spec asks
                    // for. Limit: a System Real-Time byte would also match.
                    let prevIsTimestamp = i > 1 && (b[i - 1] & 0x80) != 0
                    if prevIsTimestamp { timestampedF7 += 1 }
                    else {
                        untimestampedF7 += 1
                        if f7Examples.count < 6 {
                            let lo = max(0, i - 4), hi = min(b.count - 1, i + 1)
                            f7Examples.append("…\(hex(Array(b[lo...hi])))… at offset \(i) of \(b.count)")
                        }
                    }
                }
                if b[i] >= 0xF0 { statusCounts[b[i], default: 0] += 1 }
                i += 1
            }
        }

        print("largest packet observed : \(maxLen) bytes")
        print("total bytes received    : \(totalBytes)")
        print("")
        print("=== F7 (RAW COUNT ONLY — NOT A PARSE; see the Python analyser) ===")
        print("F7 preceded by a timestamp byte     : \(timestampedF7)")
        print("F7 NOT preceded by a timestamp byte : \(untimestampedF7)")
        for e in f7Examples { print("   \(e)") }
        print("")
        print("system bytes seen inside packets (indicative, not a parse):")
        for (k, v) in statusCounts.sorted(by: { $0.key < $1.key }) {
            print(String(format: "   %02X  x%d", k, v))
        }
        if let path = dumpPath {
            let lines = packets.map { String(format: "%.6f %@", $0.t, hex($0.bytes)) }
            try? lines.joined(separator: "\n").write(toFile: path, atomically: true,
                                                     encoding: .utf8)
            print("\nraw packets written to \(path)  (\(packets.count) lines)")
        }
        print("\n=== FIRST 15 PACKETS, RAW ===")
        for pk in packets.prefix(15) {
            print(String(format: "  %7.3f  [%2d]  %@", pk.t, pk.bytes.count, hex(pk.bytes)))
        }
        exit(0)
    }
}

let trace = Trace()
trace.start()
RunLoop.main.run()
