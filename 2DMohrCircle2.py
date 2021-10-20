import numpy as np
import matplotlib.pyplot as pl
import matplotlib.patches as patches

class element:
    def __init__(self):
        self.edgePointsX =[0.25, 3.75, 4.25, 4.25, 3.75, 0.25, -0.25, -0.25]
        self.edgePointsY = [-0.25, -0.25, 0.25, 3.75, 4.25, 4.25, 3.75, 0.25]
        self.midPointsX = [-0.25, 2, 2, 4.25]
        self.midPointsY = [2, -0.25, 4.25, 2]
        self.midOffPointsX = [-2, 2, 2, 6]
        self.midOffPointsY = [2, -2, 6, 2]
        self.allRotateablePointsX = [0.25, 3.75, 4.25, 4.25, 3.75, 0.25, -0.25, -0.25, -0.25, 2, 2, 4.25, -2, 2, 2, 6]
        self.allRotateablePointsY = [-0.25, -0.25, 0.25, 3.75, 4.25, 4.25, 3.75, 0.25, 2, -0.25, 4.25, 2, 2, -2, 6, 2]
    @classmethod
    def rotate(self,x,y,angle): #rotate x,y around xo,yo by theta (rad)
        theta = np.deg2rad(angle)
        xp, yp = [], []
        for k in range(len(x)):
            xr=np.cos(theta)*(x[k])-np.sin(theta)*(y[k])
            yr=np.sin(theta)*(x[k])+np.cos(theta)*(y[k])
            xp.append(xr)
            yp.append(yr)
        return xp, yp
    def buildElement(self, angle):
        fig = pl.figure(tight_layout=True)
        ax = fig.add_subplot(1,1,1)
        # Determine Edge Points of Square/Element
        #x = [-0.25, 4.25, 4.25, -0.25]
        #y = [-0.25, -0.25, 4.25, 4.25]
        x,y = self.rotate(self.edgePointsX, self.edgePointsY, angle)
        
        #ax.scatter(x,y)
        # Midpoints of the Square/Element
        x1, y1 = self.midPointsX, self.midPointsY#self.rotate(self.midPointsX, self.midOffPointsY, angle)
        #ax.scatter(x1, y1)
        # Midpoints that are off of
        x1, x2 = [], []
        if (angle == 0):
            x1, y1 = self.midPointsX, self.midPointsY
            x2, y2 = self.midOffPointsX, self.midOffPointsY
        else:
            x1, y1 = self.rotate(self.midPointsX, self.midPointsY, angle)
            x2, y2 = self.rotate(self.midOffPointsX, self.midOffPointsY, angle)
        #ax.scatter(x2, y2)
        ax.add_patch(patches.Rectangle((0,0), 4,4, ec='k', fc=None, color=None, angle=angle))
        centerMovementX, CenterMovementY = self.rotate([2], [2], angle)
        ax.plot([centerMovementX, [centerMovementX[0]+5]], [CenterMovementY, CenterMovementY], color='k', zorder=0 )

        #ax.arrow(0, -0.25, 4, 0, length_includes_head=True, head_width=0.2)
        # Arrow to Point Arrangement for Shear Stress Arrows
        ArrowArr = [0, 2, 4, 6]
        #print(ArrowArr)
        # List Handles are Intended to Provide Flexability with Arrows
        # Looking to figure out how to flip the direction of two arrows
        xlistHandle = x
        ylistHandle = y
        for i in ArrowArr:
            dx = x[i+1] - x[i]
            dy = y[i+1] - y[i]
            ax.arrow(x[i], y[i], dx, dy, length_includes_head=False, head_width=0.2, shape='left', color='k')
            print(x[i], y[i], dx, dy)
        
        for e in range(len(x1)):
            dx = x2[e] - x1[e]
            dy = y2[e] - y1[e]
            ax.arrow(x1[e], y1[e], dx, dy, length_includes_head=True, head_width=0.2, color='k')
        
        ax.annotate(
                r'$\tau_{xy}$',
                (x[4], y[4]),
                textcoords='offset points',
                xytext= (10,15),
                ha = 'left'
            )

        ax.set_aspect('equal')
        pl.show()

def stress(sigmax, sigmay, txy):
    # Principle Stresses

    r = (sigmax + sigmay)/2
    root = np.sqrt( ((sigmax - sigmay)/2)**2 + txy**2)

    sigma1 = r + root
    sigma2 = r - root

    return sigma1, sigma2

def buildMohrCircle(sigmax, sigmay, txy, dire, sigma1, sigma2):
    # Initialize Figure using Matplotlib.pyplot python library
    fig = pl.figure(tight_layout=True)
    ax = fig.add_subplot(1,1,1)

    # Assign the center coordinates of the Mohr Circle for Plotting Mohr Circle
    R = (sigmax + sigmay)/2
    centerCoord = (R, 0)
    # Use a tuple to store sign convention for vertical coordinate.
    signConvention = (1,1)
    if (dire == "cw"):
        signConvention = (1,-1)
    else:
        signConvention = (-1, 1)
    
    # Determine Radius of Mohr Circle
    x1 = R
    x2 = sigmax
    y1 = 0
    y2 = txy*signConvention[0]
    r = np.sqrt(((sigmax - sigmay)/2)**2 + txy**2 )
    
    # Constructing x and y arrays to carry Mohr Cricle Points of Interest
    """
    Description of Points (in order)
    - Normal stress x
    - Normal stress y
    - Center of Mohr Circle
    - First principle stress
    - Second principle stress
    """
    x = [sigmax, sigmay, R, sigma1, sigma2, sigmax,                sigmay,                sigmax,                sigmay,                R,  R]
    y = [0,      0,      0, 0,      0,      txy*signConvention[0], txy*signConvention[1], txy*signConvention[0], txy*signConvention[1], -r, +r]
    labels = [r'$\sigma_x$', r'$\sigma_y$', 'C', r'$\sigma_1$', r'$\sigma_2$', r'( $\sigma_x, \tau_{xy}$ )', r'( $\sigma_y, \tau_{xy}$ )', 'X', 'Y', r'$\tau_{min}$', r'$\tau_{max}$', ]

    # Plotting Circle
    mohrCircle = pl.Circle(centerCoord, r, fill=False)
    ax.add_artist(mohrCircle)

    # Plotting Points
    ax.scatter(x, y)

    # Build and Plot Axis Line

    # Algebra to Define Equation of Line (Will be important later to get a midpoint on line to plot curved arrow from)
    m = (y2 - y1) / (x2 - x1)
    line = lambda x: m*(x-x1) + y1
    b = line(0)
    axisLine = lambda x: m*(x-x1) + y1 + b
    # Keep on eye on this range using different values for stresses to see if it will work for all cases
    ra = np.linspace((sigmax), (sigmay), 200)

    ax.plot(ra, line(ra), color='blue')

    ax.vlines(R, -r, +r, linestyles='--')

    # Plotting Labels
    for i in range(len(labels)):
        if (labels[i] == 'X'):
            ax.annotate(
                labels[i],
                (x[i], y[i]),
                textcoords='offset points',
                xytext= (-10,15),
                ha = 'left'
            )
        elif (labels[i] == 'Y'):
            ax.annotate(
                labels[i],
                (x[i], y[i]),
                textcoords='offset points',
                xytext= (-10,15),
                ha = 'left'
            )
        else:
            ax.annotate(
                labels[i],
                (x[i], y[i]),
                textcoords='offset points',
                xytext= (10,8),
                ha = 'left'
            )
    # Plot Phi Angle Arrows
    px1 = R + (sigmax - R)/2
    px2 = R + (sigma1 - R)/2
    py1 = line(px1)

    py2 = 0

    ax.scatter([px1, px2], [py1, py2])
    curve = 0.3
    if (py1 > 0):
        curve = -0.3


    twophip = patches.FancyArrowPatch((px1, py1),(px2, py2), ArrowStyle='->, head_length=0.4, head_width=0.2', connectionstyle=f'arc3, rad={curve}')
    ax.add_patch(twophip)
        

    # Plotting Axis Lines
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.set_aspect('equal')
    pl.show()
'''
def buildMaxShearElement(x, y, t1, phis):
    x, y = rotate(x, y, 0, 0)
    print(xp)
    fig = pl.figure(tight_layout=True)
    ax = fig.add_subplot(1,1,1)
    ax.scatter(xp, yp)
    pl.show()
'''
def main():
    maxelement = element()
    sigmax = 20
    sigmay = -10
    txy = 10
    direction = "cw"

    sigma1, sigma2 = stress(sigmax, sigmay, txy)
    #buildMohrCircle(sigmax, sigmay, txy, direction, sigma1, sigma2)
    maxelement.buildElement(10)
    #buildPrincipleStressElement()
    #buildMaxShearElement(x,y, 10, 20)
    
if __name__ == "__main__": main()