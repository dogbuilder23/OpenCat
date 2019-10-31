from tkinter import *
import math
import time

def angleInRadians(angle_in_degrees):
  return angle_in_degrees * math.pi / 180

def rotatedLineEnds(start_x, start_y, length, angle_in_radians):
  return (start_x + length * math.cos(angle_in_radians), 
          start_y + length * math.sin(angle_in_radians))

def drawLine(canvas, start_x, start_y, length, angle_in_degrees, **kwargs):
  # 0 degrees = horizontal.  + degrees is clockwise.
  angle_in_radians = angle_in_degrees * math.pi / 180

  end_x = start_x + length * math.cos(angle_in_radians)
  end_y = start_y + length * math.sin(angle_in_radians)
  return canvas.create_line(start_x, start_y, end_x, end_y, kwargs) 

  
class CatBot(object):
  skills = { 'balance' : (0,  0,  0,  0,  0,  0,  0,  0, 30, 30,-30,-30, 30, 30,-30,-30),
             'buttUp'  : (20, 40,  0,  0,  5,  5,  3,  3, 90, 90,-45,-45,-60,-60, -5, -5),
             'calib'   : (0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0),
             'cd1'     : (20,-45, 30,  0,  5,  5,  3,  3, 70, 70,-45,-45,-60,-60,  0,  0),
             'cd2'     : (-30,-30,  0,  0,  5,  5,  3,  3, 70, 70,-45,-45,-60,-60,  0,  0),
             'dropped' : (0, 30,  0,  0, -5, -5, 15, 15,-75,-75,-60,-60, 60, 60, 30, 30),
             'lifted'  : (0,-70,  0,  0,  0,  0,  0,  0, 55, 55, 20, 20, 45, 45,  0,  0),
             'pee'     : (45, 20,  0,  0, 15,-10, 60,-10, 45, 45,-70,-15, 15, 45, 30,-20),
             'pee1'    : (45, 10,  0,  0, 15,-10, -5, -5, 45, 30,-30,-15, 15, 45,-30,  0),
             'pu1'     : (0,-30,  0,  0,  0,  0,  0,  0, 20, 20, 60, 60, 60, 60,-55,-55),
             'pu2'     : (0, 10,  0,  0,  0,  0,  0,  0, 60, 60, 40, 40,-45,-45,-55,-55),
             'rest'    : (-30,-80,-45,  0, -3, -3,  3,  3, 60, 60,-60,-60,-45,-45, 45, 45),
             'sit'     : (0,  0,-60,  0, -5, -5, 20, 20, 30, 30,-90,-90, 60, 60, 45, 45),
             'sleep'   : (-10,-100,  0,  0, -5, -5,  3,  3, 80, 80,-80,-80,-55,-55, 55, 55),
             'str'     : (0, 30,  0,  0, -5, -5,  0,  0,-60,-60,-15,-15, 60, 60,-45,-45)}    
  skill_names = list(sorted(skills.keys()))
  
  gaits = { 'wk' :  (14, 54,-56,-48, 21, 20,  0,-13,
                     16, 55,-64,-46, 19, 23, -8,-12,
                     20, 55,-66,-44, 17, 26,-22,-11,
                     23, 56,-65,-43, 15, 29,-29,-10,
                     26, 56,-61,-40, 14, 32,-36,-10,
                     28, 55,-58,-38, 13, 37,-41,-11,
                     31, 57,-55,-35, 12, 36,-44,-11,
                     34, 61,-56,-33, 12, 32,-41,-11,
                     36, 64,-56,-30, 11, 26,-36,-12,
                     39, 65,-56,-27, 11, 21,-33,-13,
                     41, 64,-56,-24, 11, 11,-30,-15,
                     43, 57,-56,-21, 12,  2,-27,-16,
                     45, 47,-56,-19, 12, -1,-23,-17,
                     47, 34,-55,-19, 12,  0,-21,-14,
                     49, 20,-54,-21, 14,  7,-19,-10,
                     50, 18,-53,-24, 15, 10,-17, -5,
                     52, 15,-52,-29, 16, 15,-15, -2,
                     53, 13,-50,-43, 18, 19,-14,  2,
                     54, 14,-48,-55, 20, 21,-13,  0,
                     54, 16,-46,-63, 23, 19,-12, -7,
                     55, 20,-44,-66, 25, 17,-11,-19,
                     56, 23,-43,-65, 28, 15,-10,-29,
                     56, 26,-40,-62, 31, 14,-10,-34,
                     55, 28,-38,-59, 36, 13,-11,-40,
                     57, 31,-35,-55, 36, 12,-11,-45,
                     60, 34,-33,-56, 33, 12,-11,-41,
                     64, 36,-30,-56, 26, 11,-12,-37,
                     65, 39,-27,-56, 21, 11,-13,-33,
                     65, 41,-24,-56, 13, 11,-15,-30,
                     59, 43,-21,-56,  3, 12,-16,-27,
                     49, 45,-19,-56, -1, 12,-17,-24,
                     36, 47,-19,-55,  0, 12,-14,-21,
                     21, 49,-21,-54,  6, 14,-10,-19,
                     18, 50,-24,-53, 10, 15, -5,-18,
                     15, 52,-29,-52, 14, 16, -2,-15,
                     13, 53,-43,-50, 19, 18,  2,-14,
                     13, 54,-55,-48, 21, 20,  0,-13)}
  
  def __init__(self, canvas, start_x, start_y, size):
    self.canvas = canvas
    self.start_x = start_x
    self.start_y = start_y
    self.size = size
    self.angles = CatBot.skills.get('balance')
    self.front_upper_leg = None
    self.front_lower_leg = None
    self.hind_upper_leg = None
    self.hind_lower_leg = None
    self.text = None
    self.new_text = 'balance'
    self.pose_num = 0
    self.gait = None
    self.frame = 0
    
  def legLength(self):
    return self.size * 2
  
  def frontShoulderCoords(self):
    return (self.start_x, self.start_y + self.size)
  
  def hindShoulderCoords(self):
    return (self.start_x + 4 * self.size, self.start_y + self.size)
  
  def drawFrontLeg(self, shoulder_pitch_degrees, knee_degrees):
    if self.front_upper_leg:
      self.canvas.delete(self.front_upper_leg)
    if self.front_lower_leg:
      self.canvas.delete(self.front_lower_leg)
    s_raw_deg = -1 * shoulder_pitch_degrees + 90
    (s_x, s_y) = self.frontShoulderCoords()
    (k_x, k_y) = rotatedLineEnds(s_x, s_y, self.legLength(), angleInRadians(s_raw_deg))
    k_raw_deg = s_raw_deg + 90 - knee_degrees
    self.front_upper_leg = self.canvas.create_line(s_x, s_y, k_x, k_y, width = 4)
    self.front_lower_leg = drawLine(self.canvas, k_x, k_y, self.legLength(), k_raw_deg, width = 4)
    
  def drawHindLeg(self, shoulder_pitch_degrees, knee_degrees):
    if self.hind_upper_leg:
      self.canvas.delete(self.hind_upper_leg)
    if self.hind_lower_leg:
      self.canvas.delete(self.hind_lower_leg)
    s_raw_deg = -1 * shoulder_pitch_degrees + 90
    (s_x, s_y) = self.hindShoulderCoords()
    (k_x, k_y) = rotatedLineEnds(s_x, s_y, self.legLength(), angleInRadians(s_raw_deg))
    k_raw_deg = s_raw_deg - 90 - knee_degrees
    self.hind_upper_leg = self.canvas.create_line(s_x, s_y, k_x, k_y, width = 4)
    self.hind_lower_leg = drawLine(self.canvas, k_x, k_y, self.legLength(), k_raw_deg, width = 4)
  
  def drawBody(self):
    self.canvas.create_rectangle(self.start_x, self.start_y,
                                 self.start_x + 4 * self.size, self.start_y + 2 * self.size)
    
  def setAngles(self, angles):
    self.angles = []
    self.angles.extend(angles)
  
  def setPose(self, name):
    if name in CatBot.skills:
      angles = CatBot.skills.get(name)
      self.setAngles(angles)
      self.new_text = name
      
  def drawSelf(self):
    self.drawBody()
    self.drawFrontLeg(self.angles[8], self.angles[12])
    self.drawHindLeg(self.angles[11], self.angles[15])
    if self.text:
      self.canvas.delete(self.text)
    if self.new_text:
      self.text = self.canvas.create_text(self.start_x + 2 * self.size, self.start_y - self.size, 
                                          text = self.new_text)
      self.new_text = None

  def applyPoseNum(self):
    pose_name = CatBot.skill_names[self.pose_num]
    self.setPose(pose_name)
    self.drawSelf()
    
  def applyNextHigherPose(self):
    self.pose_num = self.pose_num + 1
    if self.pose_num > len(CatBot.skill_names) - 1:
      self.pose_num = len(CatBot.skill_names) - 1
    self.applyPoseNum()
  
  def applyNextLowerPose(self):
    self.pose_num = self.pose_num - 1
    if self.pose_num < 0:
      self.pose_num = 0
    self.applyPoseNum()
    
  def keyPress(self, event):
    if event.keysym == 'Left':
      self.applyNextLowerPose()
    elif event.keysym == 'Right':
      self.applyNextHigherPose()
    
  def nextFrame(self):
    None
    #self.applyNextHigherPose()
      
class CatBotFrame(Frame):
  def __init__(self, master):
    Frame.__init__(self, master)
    self.canvas = Canvas(self, width=650, height=400)
    self.canvas.pack()
    self.catBot = CatBot(self.canvas, 225, 100, 50)
    self.canvas.bind_all('<KeyPress-Return>', self.catBot.keyPress)
    self.canvas.bind_all('<KeyPress-Up>', self.catBot.keyPress)
    self.canvas.bind_all('<KeyPress-Down>', self.catBot.keyPress)
    self.canvas.bind_all('<KeyPress-Left>', self.catBot.keyPress)
    self.canvas.bind_all('<KeyPress-Right>', self.catBot.keyPress)
    self.catBot.drawSelf()
    self.poll() # start the polling loop
    
  def poll(self):
    self.catBot.nextFrame()
    self.after(3000, self.poll)

# --------- main ------------

window = Tk()
window.title("OpenCat Poses")
frame = CatBotFrame(window)
frame.pack()
window.update()
window.mainloop()