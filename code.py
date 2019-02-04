import sys
from api import *

#######    YOUR CODE FROM HERE #######################
def level1(botId):
    moveType = 5
    botsPose = get_botPose_list()
    obstaclePose = get_obstacles_list()
    greenZone = get_greenZone_list()
    redZone = get_redZone_list()
    originalGreenZone = get_original_greenZone_list()
    while True:
        successful_move, mission_complete = send_command(botId, moveType)
        if not mission_complete:
            if not successful_move:
                moveType = 1 + (moveType+1)%8
        else:
            # The mission has been completed. You may now exit.
            # The final score will be displayed on the screen
            break

def level2(botId):
    pass

def level3(botId):
    pass

def level4(botId):
    pass

def level5(botId):
    pass

def level6(botId):
    pass


#######    DON'T EDIT ANYTHING BELOW  #######################

if  __name__=="__main__":
    botId = int(sys.argv[1])
    level = get_level()
    if level == 1:
        level1(botId)
    elif level == 2:
        level2(botId)
    elif level == 3:
        level3(botId)
    elif level == 4:
        level4(botId)
    elif level == 5:
        level5(botId)
    elif level == 6:
        level6(botId)
    else:
        print("Wrong level! Please restart and select correct level")
