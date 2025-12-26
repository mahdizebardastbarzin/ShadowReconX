# ShadowReconX
# Advanced Modular Defensive Recon & Audit Tool (CLI + GUI)
# Educational / Blue Team / Internal Audit Only

# ======================================================
# CORE IMPORTS
# ======================================================

import os
import sys
import json
import time
import platform
import socket
import getpass
import psutil
from datetime import datetime

# ======================================================
# PLUGIN SYSTEM
# ======================================================

PLUGINS = {}


def register_plugin(name, func):
    PLUGINS[name] = func


# ======================================================
# PLUGINS (SAFE ENUMERATION)
# ======================================================

def plugin_system():
    return {
        'os': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'architecture': platform.machine(),
        'hostname': socket.gethostname(),
        'user': getpass.getuser(),
        'uptime_seconds': int(time.time() - psutil.boot_time())
    }


register_plugin('System Info', plugin_system)


def plugin_cpu():
    return {
        'cores_physical': psutil.cpu_count(logical=False),
        'cores_logical': psutil.cpu_count(logical=True),
        'usage_percent': psutil.cpu_percent(interval=1)
    }


register_plugin('CPU Info', plugin_cpu)


def plugin_memory():
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'used': mem.used,
        'available': mem.available
    }


register_plugin('Memory Info', plugin_memory)


def plugin_disks():
    disks = []
    for d in psutil.disk_partitions():
        try:
            u = psutil.disk_usage(d.mountpoint)
            disks.append({
                'device': d.device,
                'mount': d.mountpoint,
                'fs': d.fstype,
                'total': u.total,
                'used': u.used
            })
        except Exception:
            pass
    return disks


register_plugin('Disk Info', plugin_disks)


def plugin_network():
    data = []
    for i in psutil.net_if_addrs():
        for a in psutil.net_if_addrs()[i]:
            data.append({
                'interface': i,
                'address': a.address,
                'family': str(a.family)
            })
    return data


register_plugin('Network Info', plugin_network)


def plugin_processes():
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'username', 'status']):
        try:
            procs.append(p.info)
        except Exception:
            pass
    return procs


register_plugin('Processes', plugin_processes)

# ======================================================
# EXECUTION ENGINE
# ======================================================


def run_all_plugins():
    results = {
        'tool': 'ShadowReconX',
        'timestamp': datetime.utcnow().isoformat(),
        'plugins': {}
    }
    for name, func in PLUGINS.items():
        results['plugins'][name] = func()
    return results


RESULTS = run_all_plugins()

# ======================================================
# EXPORT MODULE
# ======================================================


def export_json(path='shadowreconx_report.json'):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(RESULTS, f, indent=4)


def export_text(path='shadowreconx_report.txt'):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('ShadowReconX Security Audit Report\n')
        f.write('=' * 40 + '\n')
        for section, data in RESULTS['plugins'].items():
            f.write(f"\n[{section}]\n")
            if isinstance(data, list):
                for i in data:
                    f.write(str(i) + '\n')
            else:
                for k, v in data.items():
                    f.write(f"{k}: {v}\n")


# ======================================================
# CLI INTERFACE
# ======================================================

def run_cli():
    print('\n[ ShadowReconX | Modular Recon Tool ]')
    print("\n[ Powered by | Engineer Mahdi Zebardast Barzin ]")
    print("\n[ github | https://github.com/mahdizebardastbarzin ]\n")
    for section, data in RESULTS['plugins'].items():
        print(f"[{section}]")
        if isinstance(data, list):
            for i in data:
                print(i)
        else:
            for k, v in data.items():
                print(f"{k}: {v}")
        print()

    export_json()
    export_text()
    print('[+] Reports exported successfully.')


# ======================================================
# GUI (COMMERCIAL-STYLE)
# ======================================================

def run_gui():
    import tkinter as tk
    from tkinter import ttk
    from tkinter.scrolledtext import ScrolledText

    root = tk.Tk()
    root.title('ShadowReconX – Security Recon Suite')
    root.geometry('1100x650')

    style = ttk.Style()
    try:
        style.theme_use('clam')
    except Exception:
        pass

    style.configure('.', background='#0f172a', foreground='#e5e7eb')
    style.configure('TFrame', background='#0f172a')
    style.configure('TLabel', background='#0f172a', foreground='#e5e7eb')
    style.configure('TButton', background='#111827', foreground='#e5e7eb')
    style.map('TButton', background=[('active', '#1f2933')])
    style.configure('Treeview', background='#020617',
                    fieldbackground='#020617', foreground='#e5e7eb')
    style.configure('Treeview.Heading', background='#020617',
                    foreground='#93c5fd')

    header = ttk.Frame(root)
    header.pack(side='top', fill='x', pady=5)

    ttk.Label(header,
              text='ShadowReconX | Modular Recon Tool',
              font=('Segoe UI', 14, 'bold')).pack()
    ttk.Label(header,
              text='Powered by | Engineer Mahdi Zebardast Barzin',
              font=('Segoe UI', 9)).pack()
    ttk.Label(header,
              text='github | https://github.com/mahdizebardastbarzin',
              font=('Segoe UI', 9)).pack()

    ttk.Separator(root).pack(fill='x', pady=5)

    left = ttk.Frame(root, width=220)
    left.pack(side='left', fill='y')

    right = ttk.Frame(root)
    right.pack(side='right', fill='both', expand=True)

    txt = ScrolledText(right, font=('Consolas', 10))
    txt.pack(fill='both', expand=True)

    def close_view():
        txt.delete('1.0', tk.END)
        txt.insert(
            tk.END,
            '[ View closed – select another module from the sidebar ]'
        )

    def terminate_process_by_pid():
        from tkinter import messagebox, simpledialog
        try:
            pid = simpledialog.askinteger(
                'Terminate Process',
                'Enter PID to terminate:'
            )
            if pid is None:
                return
            proc = psutil.Process(pid)
            name = proc.name()
            if not messagebox.askyesno(
                'Confirm',
                f'Terminate process {name} (PID {pid})?'
            ):
                return
            proc.terminate()
            messagebox.showinfo(
                'Success',
                f'Process {name} (PID {pid}) terminated.'
            )
        except psutil.NoSuchProcess:
            messagebox.showerror('Error', 'No such process.')
        except psutil.AccessDenied:
            messagebox.showerror(
                'Error',
                'Access denied. Try running with higher privileges.'
            )
        except Exception as e:
            messagebox.showerror('Error', str(e))

    # ======================================================
    # SECTION: PROCESSES
    # ======================================================

    def show(section):
        for widget in right.winfo_children():
            widget.destroy()

        if section == 'Processes':
            from tkinter import messagebox

            frame = ttk.Frame(right)
            frame.pack(fill='both', expand=True)

            cols = ('pid', 'name', 'user', 'status', 'risk')
            tree = ttk.Treeview(
                frame,
                columns=cols,
                show='headings',
                selectmode='browse'
            )
            for c in cols:
                tree.heading(c, text=c.upper())
                tree.column(c, anchor='w')

            vsb = ttk.Scrollbar(
                frame,
                orient='vertical',
                command=tree.yview
            )
            tree.configure(yscrollcommand=vsb.set)

            hsb = ttk.Scrollbar(
                frame,
                orient='horizontal',
                command=tree.xview
            )
            tree.configure(xscrollcommand=hsb.set)
            hsb.pack(side='bottom', fill='x')

            tree.pack(side='left', fill='both', expand=True)
            vsb.pack(side='right', fill='y')

            AUDIT_LOG = os.path.join(
                os.getcwd(),
                'shadowreconx_audit.log'
            )

            def log(action, pid, name):
                with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
                    f.write(
                        f"{datetime.utcnow().isoformat()} | "
                        f"{action} | PID={pid} | {name}\n"
                    )

            suspicious_names = {
                'nc', 'netcat', 'meterpreter', 'mimikatz',
                'powershell', 'cmd', 'bash'
            }

            def risk_score(p):
                score = 0
                try:
                    if (p.name() or '').lower() in suspicious_names:
                        score += 50
                    if p.status() == psutil.STATUS_ZOMBIE:
                        score += 30
                    if p.username() in ('SYSTEM', 'root'):
                        score += 10
                    if p.cpu_percent(interval=0.0) > 50:
                        score += 10
                except Exception:
                    pass
                return min(score, 100)

            def load_processes():
                tree.delete(*tree.get_children())
                for p in psutil.process_iter(
                    ['pid', 'name', 'username', 'status']
                ):
                    try:
                        r = risk_score(p)
                        tag = 'low'
                        if r >= 70:
                            tag = 'high'
                        elif r >= 40:
                            tag = 'mid'
                        tree.insert(
                            '',
                            'end',
                            values=(p.pid, p.name(),
                                    p.username(), p.status(), r),
                            tags=(tag,)
                        )
                    except Exception:
                        pass

            tree.tag_configure('high', background='#7f1d1d')
            tree.tag_configure('mid', background='#78350f')
            tree.tag_configure('low', background='#020617')
            load_processes()

            controls = ttk.Frame(right)
            controls.pack(fill='x', pady=6)

            def selected_pid():
                sel = tree.selection()
                if not sel:
                    return None
                return int(tree.item(sel[0], 'values')[0])

            def refresh_only():
                load_processes()

            def terminate_selected():
                pid = selected_pid()
                if pid is None:
                    return
                try:
                    proc = psutil.Process(pid)
                    if not messagebox.askyesno(
                        'Confirm',
                        f'Terminate {proc.name()} (PID {pid})?'
                    ):
                        return
                    proc.terminate()
                    log('TERMINATE', pid, proc.name())
                    refresh_only()
                except Exception as e:
                    messagebox.showerror('Error', str(e))

            def kill_tree():
                pid = selected_pid()
                if pid is None:
                    return
                try:
                    parent = psutil.Process(pid)
                    procs = parent.children(recursive=True)
                    procs.append(parent)
                    if not messagebox.askyesno(
                        'Confirm',
                        f'Kill process tree of {parent.name()} (PID {pid})?'
                    ):
                        return
                    for pr in procs:
                        try:
                            pr.terminate()
                            log('KILL_TREE', pr.pid, pr.name())
                        except Exception:
                            pass
                    refresh_only()
                except Exception as e:
                    messagebox.showerror('Error', str(e))

            def suspend_selected():
                pid = selected_pid()
                if pid is None:
                    return
                try:
                    pr = psutil.Process(pid)
                    pr.suspend()
                    log('SUSPEND', pid, pr.name())
                    refresh_only()
                except Exception as e:
                    messagebox.showerror('Error', str(e))

            def resume_selected():
                pid = selected_pid()
                if pid is None:
                    return
                try:
                    pr = psutil.Process(pid)
                    pr.resume()
                    log('RESUME', pid, pr.name())
                    refresh_only()
                except Exception as e:
                    messagebox.showerror('Error', str(e))

            ttk.Button(
                controls,
                text='Refresh Processes',
                command=refresh_only
            ).pack(side='left', padx=5)
            ttk.Button(
                controls,
                text='Terminate',
                command=terminate_selected
            ).pack(side='left', padx=5)
            ttk.Button(
                controls,
                text='Kill Tree',
                command=kill_tree
            ).pack(side='left', padx=5)
            ttk.Button(
                controls,
                text='Suspend',
                command=suspend_selected
            ).pack(side='left', padx=5)
            ttk.Button(
                controls,
                text='Resume',
                command=resume_selected
            ).pack(side='left', padx=5)
            return

        # ======================================================
        # NEW SECTION: PROCESS DETAILS (FILES & NETWORK)
        # ======================================================
        if section == 'Process Details':
            frame = ttk.Frame(right)
            frame.pack(fill='both', expand=True)

            cols = ('pid', 'name', 'user', 'status', 'open_files', 'connections')
            tree = ttk.Treeview(
                frame,
                columns=cols,
                show='headings',
                selectmode='browse'
            )
            for c in cols:
                tree.heading(c, text=c.upper())
                tree.column(c, anchor='w')

            vsb = ttk.Scrollbar(
                frame,
                orient='vertical',
                command=tree.yview
            )
            tree.configure(yscrollcommand=vsb.set)

            hsb = ttk.Scrollbar(
                frame,
                orient='horizontal',
                command=tree.xview
            )
            tree.configure(xscrollcommand=hsb.set)
            hsb.pack(side='bottom', fill='x')

            tree.pack(side='left', fill='both', expand=True)
            vsb.pack(side='right', fill='y')

            def show_full_value(event):
                item = tree.identify_row(event.y)
                column = tree.identify_column(event.x)
                if not item or not column:
                    return

                col_index = int(column.replace('#', '')) - 1
                values = tree.item(item, 'values')

                # فقط برای ستون‌های open_files و connections
                if col_index not in (4, 5):
                    return

                full_text = values[col_index]

                # ساخت پنجره پاپ‌آپ
                popup = tk.Toplevel()
                popup.title("Full Details")
                popup.geometry("600x400")

                txt_popup = tk.Text(popup, wrap='word')
                txt_popup.pack(fill='both', expand=True)

                txt_popup.insert('end', full_text)
                txt_popup.config(state='disabled')

            # اتصال رویداد کلیک
            tree.bind("<Button-1>", show_full_value)

            def load_details():
                tree.delete(*tree.get_children())
                for p in psutil.process_iter(
                    ['pid', 'name', 'username', 'status']
                ):
                    try:
                        pid = p.pid
                        name = p.name()
                        user = p.username()
                        status = p.status()

                        # Open files
                        try:
                            files = [f.path for f in p.open_files()]
                            files_str = ', '.join(files) if files else 'None'
                        except Exception:
                            files_str = 'Access Denied'

                        # Network connections
                        try:
                            conns = []
                            for c in p.connections(kind='inet'):
                                laddr = (
                                    f"{c.laddr.ip}:{c.laddr.port}"
                                    if c.laddr else "-"
                                )
                                raddr = (
                                    f"{c.raddr.ip}:{c.raddr.port}"
                                    if c.raddr else "-"
                                )
                                conns.append(f"{laddr}->{raddr}")
                            conns_str = ', '.join(conns) if conns else 'None'
                        except Exception:
                            conns_str = 'Access Denied'

                        tree.insert(
                            '',
                            'end',
                            values=(
                                pid,
                                name,
                                user,
                                status,
                                files_str,
                                conns_str
                            )
                        )
                    except Exception:
                        pass

            load_details()
            return

        # DEFAULT VIEW FOR OTHER SECTIONS
        text_view = ScrolledText(right, font=('Consolas', 10))
        text_view.pack(fill='both', expand=True)
        data = RESULTS['plugins'][section]
        text_view.insert('end', f"[{section}]\n")
        if isinstance(data, list):
            for i in data:
                text_view.insert('end', f"{i}\n")
        else:
            for k, v in data.items():
                text_view.insert('end', f"{k}: {v}\n")

    ttk.Button(
        left,
        text='Close View',
        command=close_view
    ).pack(fill='x', padx=5, pady=4)

    ttk.Button(
        left,
        text='Terminate Process (PID)',
        command=terminate_process_by_pid
    ).pack(fill='x', padx=5, pady=4)

    for sec in RESULTS['plugins']:
        ttk.Button(
            left,
            text=sec,
            command=lambda s=sec: show(s)
        ).pack(fill='x', padx=5, pady=4)

    # Add the new section button
    ttk.Separator(left).pack(fill='x', padx=5, pady=10)
    ttk.Button(
        left,
        text='Process Details',
        command=lambda: show('Process Details')
    ).pack(fill='x', padx=5, pady=4)

    ttk.Separator(left).pack(fill='x', padx=5, pady=10)
    ttk.Button(
        left,
        text='Export JSON',
        command=export_json
    ).pack(fill='x', padx=5, pady=4)
    ttk.Button(
        left,
        text='Export Report',
        command=export_text
    ).pack(fill='x', padx=5, pady=4)

    root.mainloop()


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == '__main__':
    if '--gui' in sys.argv:
        run_gui()
    else:
        run_cli()

# ======================================================
# SECURITY NOTE
# ======================================================
# No exploit. No brute-force. No persistence.
# Designed for education, auditing, and blue-team use only.
