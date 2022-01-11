import csv
from PIL import Image, ImageDraw, ImageFont
import shutil, os

slist = [100, 300, 500, 700, 900, 1100]

def tc_multiplier(x):
    if x <= 300:
        return 5
    elif x >= 900:
        return 15
    else:
        return 10
    
def get_pairs(scale, alt=False, adapt=False):
    pair_list = []
    try:
        if adapt:
            file_name = 'csv/adaptive%s_alt.csv' if alt else 'csv/adaptive%s.csv'
            file = open(file_name % str(scale))
        else:
            file_name = 'csv/r%s_alt.csv' if alt else 'csv/r%s.csv'
            file = open(file_name % str(scale))
        reader = csv.reader(file)
        for row in reader:
            route_a = row[:4]
            route_b = row[4:]
            for i in range(4):
                pair_list.append((int(route_a[i]), int(route_b[i])))
        return pair_list
    except FileNotFoundError:
        print('Invalid arg: ' + str(scale))
        print('Argument must be in %s' % slist)
        
def add_units(value, i):
    unit_dict = {2: ('', ' km'), 3: ('$', '')}
    return unit_dict[i][0] + value + unit_dict[i][1]

def mins2hours(x):
    if x >= 60:
        hours = int(x / 60)
        mins = x - 60*hours
        if mins == 0:
            return '%dh' % hours
        else:
            return ('%dh %dmins' % (hours, mins))
    return str(x) + ' mins'

def create(scale, reverse=False, adaptive=False):
    # This function will generate copies of a given background image,
    # each copy having custom lines of text written on it, to represent a hypothetical choice scenario

    # Create a list to store scenario attributes
    attr_list = ['Travel Time', 'Pot. Delay', 'Distance', 'Toll Cost']

    # Format each attribute by justification to keep spacing equal
    attr_list = [i.ljust(14) for i in attr_list]

    # Open background image and store it in a variable
    im = Image.open('bg.png')
    # im = Image.new(mode='RGBA', size=im.size, color=(255, 255, 255))

    # Create text font and store in a variable
    fnt = ImageFont.truetype(font='Menlo.ttc', index=1, size=19)
    
    pair_list = get_pairs(scale, alt=reverse, adapt=adaptive)

    try:
        dir_name = 'scenario_images/adaptive%s' if adaptive else 'scenario_images/r%s'
        os.makedirs(dir_name % scale)
    except:
        pass
    
    no_of_images = 41 if adaptive else 24
    
    for i in range(no_of_images):
        x = i*4
        imc = im.copy()
        d = ImageDraw.Draw(imc)
        txt = ''
        txt += attr_list[0]
        txt += (mins2hours(pair_list[x][0]).ljust(16) + mins2hours(pair_list[x][1]) + '\n')
        
        txt += attr_list[1]
        txt += (mins2hours(pair_list[x+1][0]).ljust(16) + mins2hours(pair_list[x+1][1]) + '\n')
        
        txt += attr_list[2]
        txt += (add_units(str(pair_list[x+2][0]), 2).ljust(16) + add_units(str(pair_list[x+2][1]), 2) + '\n')
        
        txt += attr_list[3]
        txt += add_units(str(pair_list[x+3][0]), 3).ljust(16) + add_units(str(pair_list[x+3][1]), 3)
        
        d.multiline_text((10, 10), txt, fill='#8A0829', font=fnt, spacing=13, stroke_width=0) # adds text to the image
        
        if adaptive:
            file_name = 'scenario_images/adaptive%s/r%s_%s_alt.png' if reverse else 'scenario_images/adaptive%s/r%s_%s.png'
            imc.save(file_name % (scale, scale, str(10*(i+1)).zfill(2))) # saves new copy of image with added text
        else:
            file_name = 'scenario_images/r%s/r%s_%s_alt.png' if reverse else 'scenario_images/r%s/r%s_%s.png'
            imc.save(file_name % (scale, scale, str(i+1).zfill(2))) # saves new copy of image with added text
#         imc.show()
#         quit()
