import datetime
from colorama import Fore, Style, init

init(autoreset=True)

TOTAL_SLOTS = 10
VIP_SLOTS = {1, 2}

PRICING = {
    "bike": 20,
    "car": 40,
    "ev": 30,
    "heavy": 60
}

EXTRA_HOURLY_RATE = {
    "bike": 10,
    "car": 20,
    "ev": 15,
    "heavy": 30
}

class ParkingSystem:
    def __init__(self):
        self.slots = {i: None for i in range(1, TOTAL_SLOTS + 1)}
        self.revenue = 0
        self.total_vehicles = 0

    def _find_slot(self, vip=False):
        for slot, data in self.slots.items():
            if data is None:
                if vip and slot in VIP_SLOTS:
                    return slot
                if not vip and slot not in VIP_SLOTS:
                    return slot
        return None

    def vehicle_entry(self, number, v_type, vip=False):
        if v_type not in PRICING:
            print(Fore.RED + "Invalid vehicle type.")
            return

        slot = self._find_slot(vip)
        if not slot:
            print(Fore.RED + "No slot available.")
            return

        self.slots[slot] = {
            "number": number,
            "type": v_type,
            "entry_time": datetime.datetime.now()
        }
        self.total_vehicles += 1
        print(Fore.GREEN + f"Vehicle {number} parked at slot {slot}")

    def _calculate_bill(self, v_type, hours):
        cost = PRICING[v_type]
        if hours > 2:
            cost += (hours - 2) * EXTRA_HOURLY_RATE[v_type]
        return cost

    def vehicle_exit(self, slot):
        if slot not in self.slots or self.slots[slot] is None:
            print(Fore.RED + "Invalid or empty slot.")
            return

        data = self.slots[slot]
        exit_time = datetime.datetime.now()
        duration = exit_time - data["entry_time"]
        hours = max(1, int(duration.total_seconds() // 3600))

        bill = self._calculate_bill(data["type"], hours)
        self.revenue += bill
        self.slots[slot] = None

        print(Fore.CYAN + f"Vehicle {data['number']} exited.")
        print(Fore.YELLOW + f"Duration: {hours} hour(s)")
        print(Fore.GREEN + f"Bill Amount: ₹{bill}")

    def daily_report(self):
        print(Style.BRIGHT + Fore.MAGENTA + "\n--- DAILY REPORT ---")
        print(Fore.BLUE + f"Total Vehicles: {self.total_vehicles}")
        print(Fore.GREEN + f"Total Revenue: ₹{self.revenue}")

def main():
    system = ParkingSystem()

    while True:
        print("\n1. Vehicle Entry")
        print("2. Vehicle Exit")
        print("3. Daily Report")
        print("4. Exit System")

        choice = input("Choose option: ")

        if choice == "1":
            number = input("Vehicle Number: ")
            v_type = input("Type (bike/car/ev/heavy): ").lower()
            vip = input("VIP? (y/n): ").lower() == "y"
            system.vehicle_entry(number, v_type, vip)

        elif choice == "2":
            slot = int(input("Slot Number: "))
            system.vehicle_exit(slot)

        elif choice == "3":
            system.daily_report()

        elif choice == "4":
            print(Fore.GREEN + "System closed.")
            break

        else:
            print(Fore.RED + "Invalid option.")

if __name__ == "__main__":
    main()
