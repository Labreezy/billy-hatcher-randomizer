from geckolibs.gct import *
from geckolibs.geckocode import *
import random


def mission_name_to_bytestring(mission_name : str):
    return mission_name.encode("utf-8").ljust(8,b'\x00')

def shuffle_all_except(lst : list, except_list=[]):

    except_indices = [lst.index(exc) for exc in except_list]
    if len(except_indices) == 0:
        random.shuffle(lst)
        return lst
    sorted(except_indices)

    indices = [i for i in range(len(lst)) if i not in except_indices]
    random.shuffle(indices)
    for e in except_indices:
        indices.insert(e,e)
    shuffled_lst = [lst[i] for i in indices]
    return shuffled_lst



WORLD_NAMES = ['blue','red','purple','orange','yellow','green','last']
WORLDS_BASE = 0x802CB5B0
N_MISSIONS = 8
WORLD_TABLE_BASES = [WORLDS_BASE + i * 64 for i in range(len(WORLD_NAMES))]
MISSION_NAMES_BILLY = []
MISSION_NAMES_ROLLY = [wname + "6" for wname in WORLD_NAMES]
MISSION_NAMES_CHICK = [wname + "7" for wname in WORLD_NAMES]
MISSION_NAMES_BANTAM = [wname + "8" for wname in WORLD_NAMES]

for world in WORLD_NAMES:
    for i in range(5):
        if world == "last" and i == 0:
            MISSION_NAMES_BILLY.append("last")
        else:
            MISSION_NAMES_BILLY.append(f"{world}{i+1}")

SEED = input("Enter a seed number:")
SEED = int(SEED) or 0
random.seed(SEED)
MISSION_NAMES_BILLY = shuffle_all_except(MISSION_NAMES_BILLY, ['yellow3','last'])
random.shuffle(MISSION_NAMES_ROLLY)
random.shuffle(MISSION_NAMES_CHICK)
random.shuffle(MISSION_NAMES_BANTAM)
MISSION_OUT_TABLE = []
for i in range(len(WORLD_NAMES)):
    MISSION_OUT_TABLE += MISSION_NAMES_BILLY[i*5:(i+1)*5]
    MISSION_OUT_TABLE.append(MISSION_NAMES_ROLLY[i])
    MISSION_OUT_TABLE.append(MISSION_NAMES_CHICK[i])
    MISSION_OUT_TABLE.append(MISSION_NAMES_BANTAM[i])
MISSION_OUT_TABLE_BYTES = b"".join(list(map(mission_name_to_bytestring, MISSION_OUT_TABLE)))
code = WriteString(MISSION_OUT_TABLE_BYTES,WORLDS_BASE)


gct = GeckoCodeTable("GEZE8P","Billy Hatcher and the Giant Egg")
geckocode = GeckoCode(f"Billy Rando Seed {SEED}", "Labrys","Rando v0.0.2", code)
print("Gecko code:")
print(geckocode.as_text())
gct.add_child(geckocode)
open(f"GEZE8P_{SEED}.gct","wb").write(gct.as_bytes())
print(f"GCT Output to GEZE8P_{SEED}.gct.  Rename before moving!")