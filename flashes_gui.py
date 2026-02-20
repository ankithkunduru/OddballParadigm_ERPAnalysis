from psychopy import visual, core, event
import random


win = visual.Window(
    fullscr=True,
    size=[1920,1080],
    color=[-1,-1,-1],
    units='pix'
)

bbox = visual.Rect(
    win,
    width = 250,
    height = 250,
    fillColor = [-1,-1,1],
    lineColor = [-1,-1,1],
    pos = (0,0)
)

rbox = visual.Circle(
    win,
    radius = 125,
    fillColor = [1,-1,-1],
    lineColor = [1,-1,-1],
    pos = (0,0)
)

ref_box = visual.Rect(
    win,
    width = 100,
    height = 100,
    fillColor = [1,1,1],
    lineColor = [1,1,1],
    pos = (-800,450)
)

wait_text_stim = visual.TextStim(
    win=win, 
    text="Press space to continue", 
    color= [1, 0, 1], 
    height=50, 
    bold=True)


duration = 0.5
interval = 0.6
clock = core.Clock()
num_trials = 5
num_blocks = 12


if __name__ == '__main__':
    
    oddball_array = [0,0,0,0,1] #should be around 80% regular and 20% oddball
    block = 0
    index = 0
    trial = 0
    escaped = False


while block < num_blocks:
    win.flip()
    wait_text_stim.text = f"Block {block + 1} of {num_blocks}. Press space to continue."
    wait_text_stim.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in keys:
        break
    
    print (f"--- Block {block} ---")

    while trial < num_trials:
        #if escape then break
        keys = event.getKeys(['escape'])
        if 'escape' in keys:
            escaped = True
            break

        current_time = clock.getTime()

        if current_time >= interval:
            if oddball_array[index] == 1:
                rbox.draw()
            else:
                bbox.draw()
            ref_box.draw()
            win.flip()
            core.wait(duration)
            clock.reset()

            if index >= len(oddball_array) - 1:
                index = 0
                print("trial", trial, "complete", oddball_array)
                random.shuffle(oddball_array)
                trial += 1
            else:
                index += 1

        win.flip()
    
    if escaped == True:
        break
    
    block += 1
    trial = 0

win.close()
core.quit()