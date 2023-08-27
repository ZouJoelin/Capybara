
import cups

# detect printer state
def printer_state():
    conn = cups.Connection()
    printers = conn.getPrinters()
    for printer in printers:
        printer_state = printers[printer]["printer-state"]
        printer_state_reason = printers[printer]["printer-state-reasons"][0]
        # printer_state_message = printers[printer]["printer-state-message"]
        break
    ok = "none"
    door_open = "open"
    out_of_paper = "media-empty"
    out_of_toner = "toner-empty"
    jam = "jam"
    offline = "offline"
    connecting = "connecting"
    other = "other"

    print(">>>>>printer state:     ", printer_state)
    print(">>>>>state_reason:     ", printer_state_reason)
    # print(">>>>>state message:     ", printer_state_message)

    if ok == printer_state_reason:
        return "ok"
    if door_open in printer_state_reason:
        return "打印机盖未闭合"
    if out_of_paper in printer_state_reason:
        return "纸张不足"
    if out_of_toner in printer_state_reason:
        return "墨粉不足"
    if jam in printer_state_reason:
        return "有纸张堵塞"
    if offline in printer_state_reason or connecting in printer_state_reason:
        return "未连接打印机"
    else:
        return "未知错误"
    
print(printer_state())