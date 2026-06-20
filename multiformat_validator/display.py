import os
import time
import threading
import sys

from colorama import Fore, Style

# 全局输出锁
print_lock = threading.Lock()

def thread_safe_print(message: str, end: str = "\n", flush: bool = True):
    """确保在多线程下控制台输出不会发生交织错乱"""
    with print_lock:
        sys.stdout.write(message + end)
        if flush:
            sys.stdout.flush()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_progress_bar(i18n, duration=1.5):
    print(f"\n{i18n.get('validating')}")
    print(f"{i18n.get('progress')}: ", end="", flush=True)
    for i in range(21):
        bar = "█" * i + "░" * (20 - i)
        percent = i * 5
        print(f"\r{i18n.get('progress')}: [{bar}] {percent}%", end="", flush=True)
        time.sleep(duration / 20)
    print()


def display_report(i18n, result, file_path):
    clear_screen()
    if result["valid"]:
        print(f"\n{Fore.GREEN}{i18n.get('validation_passed')}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}{i18n.get('validation_failed')}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {i18n.get('report_title')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  File: {file_path}{Style.RESET_ALL}\n")
        for error in result["errors"]:
            print(f"  {Fore.RED}{i18n.get('error_type')}: {error['type']}{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}{i18n.get('error_line')}: {error['line']}, {i18n.get('error_col')}: {error['col']}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}{i18n.get('error_message')}: {error['message']}{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}{i18n.get('error_fix')}: {error['fix']}{Style.RESET_ALL}")
            print()


def display_batch_results(i18n, results):
    clear_screen()
    valid_count = sum(1 for r in results if r["valid"])
    invalid_count = len(results) - valid_count

    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  {i18n.get('batch_scan_results')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")
    print(f"  {i18n.get('total_files')}: {len(results)}")
    print(f"  {Fore.GREEN}{i18n.get('valid_files')}: {valid_count}{Style.RESET_ALL}")
    print(f"  {Fore.RED}{i18n.get('invalid_files')}: {invalid_count}{Style.RESET_ALL}\n")

    for r in results:
        status = f"{Fore.GREEN}✓" if r["valid"] else f"{Fore.RED}✗"
        print(f"  {status} {r['file']}{Style.RESET_ALL}")


