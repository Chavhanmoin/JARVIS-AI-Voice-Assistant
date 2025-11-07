import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from system_control import change_volume, change_brightness

print("\n=== 🔊🌞 TESTING 0–100 UNIT SYSTEM CONTROL (Final Version) ===")

print("\n➡️ Increasing Volume by 20% ...")
change_volume("up", 20)
time.sleep(1)

print("\n➡️ Decreasing Volume by 10% ...")
change_volume("down", 10)
time.sleep(1)

print("\n➡️ Muting Volume ...")
change_volume("mute")
time.sleep(1)

print("\n➡️ Setting Volume to 40% ...")
change_volume("set", 40)
time.sleep(1)

print("\n➡️ Increasing Brightness by 20% ...")
change_brightness("up", 20)
time.sleep(1)

print("\n➡️ Decreasing Brightness by 10% ...")
change_brightness("down", 10)
time.sleep(1)

print("\n➡️ Setting Brightness to 50% ...")
change_brightness("set", 50)
time.sleep(1)

print("\n✅ TEST COMPLETED SUCCESSFULLY!")
