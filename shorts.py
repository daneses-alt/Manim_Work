from PIL import Image
from cgi import print_arguments
from contextlib import nullcontext
import math
from manim import *
from sympy import false, mathematica_code
import manimpango
from reactive_manim import *

import numpy as np
from manim_fonts import *
from mpmath import mp
from manim import *
import numpy as np
from matplotlib.path import Path as MplPath


class Card(ThreeDScene):
    def construct(self):
        init1=Text("\"Some infinities are larger than others\"").shift(UP)
        init2=Text("\"There are different kinds of infinities\"").shift(DOWN)
        self.play(Write(init1), Wait(0.5))
        self.play(Write(init2))
        self.play(ApplyMethod(init2[9:18].set_color, RED), ApplyMethod(init1[18:24].set_color, RED), run_time=2)
        self.play(Wait(1))
        self.play(Unwrite(init1), Unwrite(init2), run_time=1)
        grid = NumberPlane((-10, 10), (-5, 5))
        #self.add(grid)
        dit= dict()
        g=[]
        numlis=[]
        for i in range(1, 11):
            dit["{0}".format(i)]= Tex( (str)(i) ).shift([-5.2+i*1.1, 2, 0]).scale(1.2)
            numlis.append( Write(dit["{0}".format(i)]) )
            self.add(dit["{0}".format(i)])
            dit["{0}".format(i)]
            if(i%2==0):
                dit["{0}".format(i)].add_updater(lambda mob, dt: mob.set_color(
                ManimColor([(int)( 255-(mob.get_y()-2)*130),(int)( 255-(mob.get_y()-2)*50), (int)(255-(mob.get_y()-2)*20) ]) ) )
                g.append(dit["{0}".format(i)].animate.shift([0, 1, 0]))
               
            else:
                dit["{0}".format(i)].add_updater(lambda mob, dt: mob.set_color(
                ManimColor([(int)( 255+(mob.get_y()-2)*20),(int)( 255+(mob.get_y()-2)*150), (int)(255+(mob.get_y()-2)*130) ]) ) )
                g.append(dit["{0}".format(i)].animate.shift([0, -1, 0]))
        gp= AnimationGroup(*g, run_time=1.5 )
        Set=Tex("$\mathbb{N} \hspace{2mm}$=", font_size=70).shift([-5.7,2,0])
        Set2=Tex("$...$", font_size=70).shift([6.4,1.8,0])
        numlis.append(Write(Set2))
        Card=Tex(r"$ | \mathbb{N} | = \aleph_0 $", font_size=55).shift(LEFT*5.26+UP*0.6 )
        NL=NumberLine([-3.5, 3.5], 10.5, include_numbers=True, font_size=50, tick_size=0.2, ).shift([1.1, -1.5, 0]) #arrows
        R=Tex("$ \mathbb{R} \hspace{2mm}$=", font_size=70).shift([-5.65, -1.5, 0])
        Card2=Tex(r"$ | \mathbb{R} | = \aleph_1 $", font_size=55).shift(LEFT*5.26, [0, -3, 0])
        Arr=Arrow(start=[-3,0,0], end=[-3, -1, 0], stroke_width=10)
        pp=DecimalNumber(0, 3, include_sign=True).shift([-0.7, 0.3, 0])
        pp.add_updater(lambda mob, dt: mob.set_value( (mob.get_x()-1.1)/1.505 ) )
        pp.add_updater(lambda mob, dt: mob.set_x( (Arr.get_x()) ) )
        self.play(Wait(0.3))
        self.play(Write(Set), LaggedStart(*numlis, lag_ratio=0.1))
        self.play(Wait(1))
        self.play(Write(Card)) 
        self.play(Wait(1))
        self.play(Write(R), Write(NL))
        self.play(Wait(0.5))
        self.play(Write(pp), Write(Arr))
        #self.add(pp, R, NL, Set, Card, Card2, Arr)
        self.play(Write(Card2))
        Card.target=Tex(r"$\aleph_0 \hspace{1mm} \neq$", font_size=80).shift([-1,1,0])
        Card2.target=Tex(r"$\aleph_1$", font_size=80).shift([1,1,0])
        l=[]
        for i in range(1,11):
            l.append(Unwrite(dit["{0}".format(i)]))
        AG=AnimationGroup(*l)
        pp.set_value(pp.get_value())
        self.play(LaggedStart(Unwrite(pp), Unwrite(Set2), Unwrite(R), Unwrite(NL), Unwrite(Set), 
                 AG, Unwrite(Arr), Transform(Card, Card.target), Transform(Card2, Card2.target) ) )
        self.play(Unwrite(Card2), Unwrite(Card))
class N(ThreeDScene):
    def construct(self):
        q1=Tex(r"$| \mathbb{N} |$", font_size=80).shift([-1,1,0])
        q2=Tex(r"$=$", font_size=80).shift([-0.1,1,0])
        q3=Tex(r"$| \mathbb{N}^2 |$", font_size=80).shift([1,1,0])
        nat=Tex(r"$1, 2, 3, 4, 5, 6, ...$", color=RED).shift([-1, 3, 0]).set_fill(color=RED, opacity=1)
        grid=NumberPlane((-3, 3), (-3, 3), x_length=14, y_length=14).scale(0.3).shift(DOWN*2+RIGHT*1.42)
        grid2 = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],x_length=14, y_length=14,
                    axis_config={"numbers_to_include": np.arange(-3,4, 1), "font_size": 34}, tips=False,).scale(0.3).shift(DOWN*2+RIGHT*1.5)
        self.play(Write(q1), Write(q2), Write(q3))
        self.play(q1.animate.set_color(RED), Write(nat))
        self.play(q3.animate.set_color(BLUE), FadeIn(grid), FadeIn(grid2)) 
        #self.play(FadeIn(grid), FadeIn(grid2))
        self.play(Wait(2))
        

class Lat(ThreeDScene):
    def construct(self):
        grid = NumberPlane((-7, 7), (-7, 7), x_length=14, y_length=14)
        grid2 = Axes(
            x_range=[-7, 7, 1],  # step size determines num_decimal_places.
            y_range=[-7, 7, 1],
            x_length=14,
            y_length=14,
            axis_config={
                "numbers_to_include": np.arange(-7,8, 1),
                "font_size": 34
            },
            tips=False,
        )
        d=dict()
        an=[]
        for i in range(-7, 8):
            for j in range(-4, 5):
                d["{}{}".format(i,j)] = Circle(0.07, color=BLUE).shift([i, j, 0]).set_fill(BLUE, opacity=1).scale(0.9999)
                #self.add( d["{}{}".format(i,j)] )
                an.append(Create( d["{}{}".format(i,j)] ) )
        #self.play(Wait(1))
        self.play( FadeIn(grid, grid2), LaggedStart(*an, lag_ratio=0.02, run_time=3))
        dit= dict()
        g=[]
        for i in range(1, 11):
            dit["{0}".format(i)]= Tex( (str)(i), color=GREEN_E ).shift([i-1, 0.3, 0]).scale(0.7)
            g.append(Write(dit["{0}".format(i)] ) )
            if(i<=8):
                g.append(d["{}0".format(i-1)].animate.set_color(GREEN))
        self.play(LaggedStart(*g, lag_ratio=0.3), run_time=4)
        an.clear()
        for i in range(-7, 8):
            for j in range(-4, 5):
                if(j!=0 or i<0):
                    self.add(d["{}{}".format(i,j)])
                    d["{}{}".format(i,j)].add_updater(lambda mob, dt: mob.set_color(
                ManimColor([(int)( 252-(0.14-mob.height/2)*170/0.07),(int)( 98-(0.14-mob.height/2)*(-90)/0.07), (int)(85-(0.14-mob.height/2)*(-140)/0.07) ]) ) )
                    an.append( d["{}{}".format(i,j)].animate.scale(2))
        gp=AnimationGroup(*an, run_time=2)
        an.append(Wait(1))
        self.play(Wait(1), gp)
        an2=[]
        for i in range(-7, 8):
            for j in range(-4, 5):
                if(j!=0 or i<0):
                    an2.append( d["{}{}".format(i,j)].animate.scale(0.5))
        self.play(*an2, run_time=4)
        self.play(Wait(2))

class Inf_Bijections(MovingCameraScene):
    def construct(self):
        grid = NumberPlane((-11, 11), (-11, 11), x_length=22, y_length=22, color=BLUE)
        grid2 = Axes(
            x_range=[-11, 11, 1],  # step size determines num_decimal_places.
            y_range=[-11, 11, 1],
            x_length=22,
            y_length=22,
            axis_config={
                "numbers_to_include": np.arange(-11,12, 1),
                "font_size": 34
            },
            tips=False,
            color=BLUE
        )
        d=dict()
        self.add(grid, grid2)
        an=[]
        for i in range(-11, 12):
            for j in range(-7, 8):
                d["{}{}".format(i,j)] = Circle(0.07, color=BLUE).shift([i, j, 0]).set_fill(BLUE, opacity=1)
                self.add( d["{}{}".format(i,j)] )
        dit= dict()
        g=[]
        for i in range(1, 11):
            dit["{0}".format(i)]= Tex(r"$\textbf{"+(str)(i)+r"}$", color=GREEN_E).shift([i-1, 0.3, 0]).scale(0.8)
            g.append(Write(dit["{0}".format(i)] ) )
            if(i<=8):
                g.append(d["{}0".format(i-1)].animate.set_color(GREEN))
        self.play(LaggedStart(*g, lag_ratio=0.3), run_time=4)
        for i in range(-7, 8):
            for j in range(-4, 5):
                if(j!=0 or i<0):
                    self.add(d["{}{}".format(i,j)])
                    d["{}{}".format(i,j)].add_updater(lambda mob, dt: mob.set_color(
                ManimColor([(int)( 252-(0.14-mob.height/2)*170/0.07),(int)( 98-(0.14-mob.height/2)*(-90)/0.07), (int)(85-(0.14-mob.height/2)*(-140)/0.07) ]) ) )
                    an.append( d["{}{}".format(i,j)].animate.scale(2))
        gp=AnimationGroup(*an, run_time=1)
        self.play(gp)
        an2=[]
        for i in range(-7, 8):
            for j in range(-4, 5):
                if(j!=0 or i<0):
                    an2.append( d["{}{}".format(i,j)].animate.scale(0.5))
        g.clear()
        for i in range(1,11):
            g.append(Unwrite(dit["{0}".format(11-i)] ) )
            if(i>=3):
                g.append(d["{}0".format(10-i)].animate.set_color(BLUE))
        self.play(LaggedStart(*g, lag_ratio=0.3), *an2, run_time=2)
        self.play(Wait(2))
        g.clear()
        fin=dict()
        x1=0
        y1=0
        for i in range(1, 10):
            for j in range(1, i+1):
                a=Tex(r"$\textbf{"+(str)((i-1)*(i)+j)+r"}$", color=GREEN_E).shift([x1, y1+0.3, 0]).set_color(GREEN_E).scale(0.75)
                #g.append(Write(a) )
                d["{}{}".format(x1, y1)].clear_updaters()
                g.append(LaggedStart( d["{}{}".format(x1, y1)].animate.set_color(GREEN_E), Write(a), lag_ratio=0.2) )
                #g.append(Write( Arrow(start=[x1,y1,0], end=[x1-1+(i%2)*2, y1, 0], color=GREEN)) )
                #arrows = [Arrow(2 * LEFT, 2 * RIGHT), Arrow(2 * DR, 2 * UL)]
                #VGroup(*arrows).set_x(0).arrange(buff=2)
                #self.play(GrowArrow(arrows[0]))
                #self.play(GrowArrow(arrows[1], point_color=RED))
                g.append(Write(Line(start=[x1,y1,0], end=[x1-1+(i%2)*2, y1, 0], color=GREEN_E,  stroke_width=3)))
                if(i%2==1):
                    x1+=1
                else:
                    x1-=1
            for j in range(1, i+1):
                a=Tex(r"$\textbf{"+(str)((i-1)*(i)+j+i)+r"}$", color=GREEN_E).shift([x1, y1+0.3, 0]).set_color(GREEN_E).scale(0.75)
               # g.append(Write(a) )
                d["{}{}".format(x1, y1)].clear_updaters()
                g.append(LaggedStart(d["{}{}".format(x1, y1)].animate.set_color(GREEN_E), Write(a) ) )
                #g.append(Write( Arrow(start=[x1,y1,0], end=[x1, y1-1+(i%2)*2, 0], color=GREEN)) )
                g.append(Write(Line(start=[x1,y1,0], end=[x1, y1-1+(i%2)*2, 0], color=GREEN_E, stroke_width=3)))
                if(i==7 and j==2):
                    g.append(self.camera.frame.animate.set(width=18))
                if(i%2==1):
                    y1+=1
                else:
                    y1-=1
        self.play(LaggedStart(grid.animate.set_opacity(0.5), grid2.animate.set_opacity(0.3), run_time=10), LaggedStart(*g, lag_ratio=0.2) )
        
        #self.play(self.camera.frame.animate.set(width=20) )





class Diag(ThreeDScene):
    def construct(self):
        q1=Tex(r"$| \mathbb{R} |$", font_size=80).shift([-1,1,0])
        q2=Tex(r"$=$", font_size=80).shift([-0.1,1,0])
        q3=Tex(r"$| \mathbb{R}^2 |$", font_size=80).shift([1,1,0])
        self.play(Write(q1), Write(q2), Write(q3)) 
        #self.play(FadeIn(grid), FadeIn(grid2))
        NL=NumberLine([-3.5, 3.5], 10.5, include_numbers=True, font_size=50, tick_size=0.2, ).shift([1.5, 2.5, 0]) #arrows
        Arr=Arrow(start=[-2,3.2,0], end=[-2, 2, 0], stroke_width=50, color=WHITE)
        pp=DecimalNumber(0, 3, include_sign=True).shift([-1.3, 3.5, 0])
        pp.add_updater(lambda mob, dt: mob.set_value( (mob.get_x()-1.5)/1.505 ) )
        pp.add_updater(lambda mob, dt: mob.set_x( (Arr.get_x()) ) )
        self.add(NL, Arr, pp)
        self.play(Write(Arr))
        self.play(q1.animate.shift([-5,-0.5,0]), q2.animate.shift([-5,-0.5,0]), q3.animate.shift([-5,-0.5,0]))
        self.play( Arr.animate.shift([2,0,0]), run_time=3)
        grid=NumberPlane((-3, 3), (-3, 3), x_length=14, y_length=14).scale(0.3).shift(DOWN*2+RIGHT*1.42)
        grid2 = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],x_length=14, y_length=14,
                    axis_config={"numbers_to_include": np.arange(-3,4, 1), "font_size": 34}, tips=False,).scale(0.3).shift(DOWN*2+RIGHT*1.5)
        #self.play(q1.animate.set_color(RED), Write(nat))
        self.play(q3.animate.set_color(BLUE), FadeIn(grid), FadeIn(grid2))




class symbols(ThreeDScene):
    def construct(self):
        sum=MathTex(r"\sum_{n \exists S}", font_size=130).shift([-3,0,0])
        sig=MathTex(r"\sigma", font_size=130).next_to(sum, RIGHT)
        parens=MathTex(r"( \partial \hspace{4mm}  )", font_size=130).next_to(sig, RIGHT)
        parens.target=MathTex("")
        h=MathTex(r"\mathcal{H}", font_size=130).next_to(sa, RIGHT*7)
        sa=MathTex(r"\sphericalangle", font_size=130).next_to(h, RIGHT).rotate(PI/5.6)

        d=MathTex(r"\partial", font_size=50).next_to(sum, DOWN*0.75).shift([-0.87,0,0])
        ele=MathTex(r"\in", font_size=60).next_to(d, RIGHT*0.6)
        ele.target=(MathTex(""))
        s=MathTex(r"\mathbb{S}", font_size=60).next_to(ele, RIGHT*0.6)
        union=MathTex(r"\cup", font_size=60).next_to(s, RIGHT*0.6)
        union.target=(MathTex(""))
        secs=MathTex(r"\mathbb{S}", font_size=60).next_to(union, RIGHT*0.6)
        secs.target=(MathTex(""))
        perp=MathTex(r"\perp", font_size=27).next_to(secs, RIGHT*0.3).shift([0,-0.2,0])

        sum.target=MathTex(r"\sum", font_size=120).rotate(-PI/2).shift([-3,-2,0])
        sa.target=MathTex(r"\sphericalangle", font_size=210).rotate(-PI/2).next_to(sum.target, RIGHT*1.8)
        perp.target=MathTex(r"\perp", font_size=200).rotate(PI).next_to(sa.target, RIGHT)
        s.target=MathTex(r"\mathbb{S}", font_size=200).shift([-1.7,0,0])
        sig.target=MathTex(r"\sigma", font_size=200).rotate(-PI/3).next_to(s.target, RIGHT).shift([0,-0.23,0])
        d.target=MathTex(r"\partial", font_size=200).next_to(sig.target, RIGHT).shift([0,0.23,0])
        h.target=MathTex(r"\mathcal{H}", font_size=200).next_to(perp.target, RIGHT)
        self.add(sum, sa, sig, perp, s, d, h, ele, union, secs, parens)
        self.play(Wait(1))
        l=[]
        for m in self.mobjects:
            l.append(Transform(m, m.target))
        g=AnimationGroup(*l)
        self.play(g)


class reals(ThreeDScene):
    def construct(self):
        d=MathTex()

        NL=NumberLine([-4.5, 4.5], 10.5, include_numbers=True, font_size=50, tick_size=0.2, ) #arrows
        R=Tex("$ \mathbb{R} \hspace{2mm}$=", font_size=70).shift([-5.65, -1.5, 0])
        Card2=Tex(r"$ | \mathbb{R} | = \aleph_1 $", font_size=55).shift(LEFT*5.26, [0, -3, 0])
        pt=Circle(radius=0.1, color=BLUE)
        pp=DecimalNumber(0, 3, include_sign=True).shift([-0.7, 0.3, 0])
        pp.add_updater(lambda mob, dt: mob.set_value( (mob.get_x()-1.1)/1.505 ) )
        pp.add_updater(lambda mob, dt: mob.set_x( (pt.get_x()) ) )
        self.add(NL, R, Card2, pt, pp)
        self.play(pt.animate.shift([5,0,0]))

from manim import *

class Moving(Scene):
    def construct(self):
        # Step 1: Create the number line
        number_line = NumberLine(
            x_range=[-7, 7],  # Set the range of the number line
            length=14,        # Length of the number line
            label_direction=UP,  # Direction of the labels
            include_numbers=True, font_size=50, tick_size=0.2
        )
        
        # Step 2: Create a moving point on the number line
        mp = Dot(color=BLUE).shift(number_line.n2p(0)+LEFT*5)  # Initially at 0
        pp=DecimalNumber(0, 2, include_sign=False).shift([-4, -0.3, 0])
        pp.add_updater(lambda mob, dt: mob.set_value( (mob.get_x()) ) )
        pp.add_updater(lambda mob, dt: mob.set_x( (mp.get_x()) ) )
        
        # Step 3: Create a 2D XY grid
        grid = NumberPlane(
            x_range=[-7, 7],
            y_range=[-5, 5],
            axis_config={"stroke_color": BLUE},
        )
        
        # Step 4: Create a new point in 2D space
        np = Dot(color=RED).shift(grid.c2p(0, 0))  # Initially at (0, 0)
        pp21=DecimalNumber(0, 2, include_sign=True).shift([-0.7, 0.3, 0])
        pp21.add_updater(lambda mob, dt: mob.set_value( (mob.get_x()) ) )
        pp21.add_updater(lambda mob, dt: mob.set_x( (np.get_x()-0.7) ) )
        pp21.add_updater(lambda mob, dt: mob.set_y( (np.get_y())+0.4) )
        pp22=DecimalNumber(0, 2, include_sign=True).shift([-0.7, 0.3, 0])
        pp22.add_updater(lambda mob, dt: mob.set_value( (mob.get_y()) ) )
        pp22.add_updater(lambda mob, dt: mob.set_x( (np.get_x()+0.7) ) )
        pp22.add_updater(lambda mob, dt: mob.set_y( (np.get_y()+0.4) ) )
        comma=Tex(",")
        comma.add_updater(lambda mob, dt: mob.set_x( (np.get_x()) ) )
        comma.add_updater(lambda mob, dt: mob.set_y( (np.get_y()+0.2) ) )
        
        # Step 5: Add everything to the scene
        self.play(Create(number_line), Create(mp), Write(pp))
        self.wait(1)
        
        # Step 6: Animate the moving point across the number line
        self.play(mp.animate.shift([7,0,0]))
        
        # Step 7: Add the grid to the scene and animate the red point
        self.play(Create(grid))
        self.play(Create(np), Write(pp21), Write(pp22), Write(comma))
        
        # Step 8: Animate the red point moving across the 2D space
        for x in range(1, 3):
            for y in range(-2, 5):
                # Animate the red point moving in 2D space
                self.play(np.animate.move_to(grid.c2p(x, y)))
        self.play(number_line.animate.set_color(RED))
        self.play(FadeIn(Rectangle(height=10, width=20, color=RED).set_fill(opacity=0.7)  ))
class m2(Scene):
    def construct(self):
        map1=MathTex(r"(x) \hspace{2mm} ", font_size=80).shift([-2,0,0])
        map2=MathTex(r"\mapsto \hspace{2mm} ", font_size=80)
        map3=MathTex(r"(y , z) \hspace{2mm} ", font_size=80).shift([2.5,0,0])
        self.add(map1, map2, map3)
        dit1=dict()
        dit2=dict()
        dit3=dict()
        for i in range(-3,5):
            if(i==-3):
                dit1["{0}".format(i)]= MathTex(r"\ldots").shift([-2,-2,0])
                dit2["{0}".format(i)]= MathTex(r"\ldots").shift([-2,0,0])
                dit3["{0}".format(i)]= MathTex(r"\ldots").shift([-2,2,0])
            elif(i==4):
                dit1["{0}".format(i)]= MathTex(r"\ldots").next_to(dit1["{0}".format(i-1)], LEFT*0.8)
                dit2["{0}".format(i)]= MathTex(r"\ldots").next_to(dit2["{0}".format(i-1)], LEFT*0.8)
                dit3["{0}".format(i)]= MathTex(r"\ldots").next_to(dit3["{0}".format(i-1)], LEFT*0.8)
            elif(i==0):
                dit1["{0}".format(i)]= MathTex(r".").next_to(dit1["{0}".format(i-1)], LEFT*0.3+DOWN*0.03)
                dit2["{0}".format(i)]= MathTex(r".").next_to(dit2["{0}".format(i-1)],  LEFT*0.3+DOWN*0.03)
                dit3["{0}".format(i)]= MathTex(r".").next_to(dit3["{0}".format(i-1)],  LEFT*0.3+DOWN*0.03)
            elif(i<0):
                dit1["{0}".format(i)]= MathTex(r"x_{{{0}}}".format(i)).next_to(dit1["{0}".format(i-1)], LEFT*0.8)
                dit2["{0}".format(i)]= MathTex(r"y_{{{0}}}".format(i)).next_to(dit2["{0}".format(i-1)], LEFT*0.8)
                dit3["{0}".format(i)]= MathTex(r"z_{{{0}}}".format(i)).next_to(dit3["{0}".format(i-1)], LEFT*0.8)
            elif(i==1):
                dit1["{0}".format(i)]= MathTex(r"x_{0}".format(i-1)).next_to(dit1["{0}".format(i-1)], LEFT*0.3+UP*0.03)
                dit2["{0}".format(i)]= MathTex(r"y_{0}".format(i-1)).next_to(dit2["{0}".format(i-1)], LEFT*0.3+UP*0.03)
                dit3["{0}".format(i)]= MathTex(r"z_{0}".format(i-1)).next_to(dit3["{0}".format(i-1)], LEFT*0.3+UP*0.03)
            else:
                dit1["{0}".format(i)]= MathTex(r"x_{0}".format(i-1)).next_to(dit1["{0}".format(i-1)], LEFT*0.6)
                dit2["{0}".format(i)]= MathTex(r"y_{0}".format(i-1)).next_to(dit2["{0}".format(i-1)], LEFT*0.6)
                dit3["{0}".format(i)]= MathTex(r"z_{0}".format(i-1)).next_to(dit3["{0}".format(i-1)], LEFT*0.6)
            self.add(dit1["{0}".format(i)], dit2["{0}".format(i)], dit3["{0}".format(i)])
            #self.play(Create(dit1["{0}".format(i)]), Create(dit2["{0}".format(i)]), Create(dit3["{0}".format(i)]))
        

        ls=[]
        ls2=[]
        for i in range(-2, 4):
            if(i<0):
                if((i+10)%2==0):
                    ls.append(dit1["{0}".format(i)].animate.set_color(BLUE_C))
                else:
                    ls2.append(dit1["{0}".format(i)].animate.set_color(RED_C))
            if(i>0):
                if(i%2==1):
                    ls.append(dit1["{0}".format(i)].animate.set_color(BLUE_C))
                else:
                    ls2.append(dit1["{0}".format(i)].animate.set_color(RED_C))
            ls.append(dit2["{0}".format(i)].animate.set_color(BLUE_C))
            ls2.append(dit3["{0}".format(i)].animate.set_color(RED_C))
        self.play(AnimationGroup(*ls2), AnimationGroup(*ls))
       
        self.play(Wait(1))
        t=Tex("3.14159265...")
        self.play(Write(t))
        ls.clear
        ls2.clear
        for i in range(0, 8):
            if(i<1):
                ls.add()
            if(i>1):
                ls
def pin(n):
    mp.dps = n + 1  # Set the desired precision
    return str(mp.pi)[n]
class PiDigitsScene(Scene):
    def construct(self):
        # First 10 digits of pi
        pi_digits = "3.141592653"
        d=dict()
        for i in range(0, 10):
            d["{0}".format(i)]= Term(pin(i)).set_color(BLUE)
        digits_text = MathTex(*d).scale(0.7)
        digits_text.to_edge(UP)
        g=DGroup(digits_text)
        self.add(g)
        
        # Display the digits of Pi
        #self.play(Write(digits_text))
        
        # Create the color animation: odd place numbers turn blue, even place numbers turn red
        # Animate the color changes
        ls1=[]
        ls2=[]
        for i in range(0,10):
            if( i!=1 and (i==0 or i%2==1) ):
                ls1.append(digits_text[i:i+1].animate.set_color(BLUE))
            elif(i!=1):
                ls2.append(digits_text[i:i+1].animate.set_color(RED))
        #self.play(*[ApplyMethod(char.set_color, BLUE) if (i+100) % 2 == 0 else ApplyMethod(char.set_color, RED) for i, char in enumerate(digits_text) if char!='.'])
        #self.play(AnimationGroup(*ls1, *ls2))
        t1=MathTex(MathMatrix( [ [d["0"]] ]), d["2"], d["4"]).shift([-1,-1,0])
        #d["0"].set_tex_string("0")
        self.play(TransformInStages.from_copy(g, t1[0],      lag_ratio=0.4, run_time=2.5))
        # Wait for a moment befo

class MatrixScene(Scene):
    def construct(self):

        y0, y1 = Term("y", subscript=0), Term("y", subscript=1)
        x0, x1 = Term("x", subscript=0), Term("x", subscript=1)

        w00, w01 = Term("w", subscript="00"), Term("w", subscript="01")
        w10, w11 = Term("w", subscript="10"), Term("w", subscript="11")

        tex1 = MathTex(y0, "=", w00, x0, "+", w01, x1)
        tex2 = MathTex(y1, "=", w10, x0, "+", w11, x1)

        group = DGroup(tex1, tex2).arrange(DOWN).shift(UP)
        self.add(group).wait(2)

        tex3 = MathTex(
            MathMatrix([
                [ y0 ],
                [ y1 ]
            ]), 
            "=",
            MathMatrix([
                [ w00, w01 ],
                [ w10, w11 ]
            ]),
            MathMatrix([
                [ x0 ],
                [ x1 ]
            ])
        )
        tex3.shift(DOWN)
        
        self.play(TransformInStages.from_copy(group, tex3[0],      lag_ratio=0.4, run_time=2.5))
        self.play(TransformInStages.from_copy(group, tex3[1],      lag_ratio=0.4, run_time=1.4))
        self.play(TransformInStages.from_copy(group, tex3[2],      lag_ratio=0.4, run_time=2.5))
        self.play(TransformInStages.from_copy(group, tex3[3] - x0, lag_ratio=0.4, run_time=2.5))
        self.play(TransformInStages.from_copy(group, x0,           lag_ratio=0.4, run_time=2.5))
        self.wait(2)




class StokesVisual(MovingCameraScene):

    def functiontopmin(x, topf):
        min=-7.11
        max=-5.25
        while(math.fabs(  topf.get_point_from_function((min+max)/2)[1]-x )>0.001):
            if(topf.get_point_from_function((min+max)/2)[1]-x>0):
                max=(min+max)/2
            
            else:
                min=(min+max)/2
            if(max-min<0.01):
                break
        return min


    def functionbotmin(x, topf):
        min=-7.11
        max=0
        while(math.fabs(  topf.get_point_from_function((min+max)/2)[1]  -x )>0.001):
            #print(str(min)+ "alala "+str(max))
            if(topf.get_point_from_function((min+max)/2)[1]-x<0):
                max=(min+max)/2
            else:
                min=(min+max)/2
            if(max-min<0.01):
                break
        return min
    
    def functiontopmax(x, topf):
        min=-5.25
        max=3.58
        while(math.fabs(  topf.get_point_from_function((min+max)/2)[1]-x )>0.001):
            if(topf.get_point_from_function((min+max)/2)[1]-x<0):
                max=(min+max)/2
            else:
                min=(min+max)/2
            if(max-min<0.01):
                break
        return min


    def functionbotmax(x, topf):
        min=0
        max=3.58
        while(math.fabs(  topf.get_point_from_function((min+max)/2)[1]-x )>0.001):
            if(topf.get_point_from_function((min+max)/2)[1]-x>0):
                max=(min+max)/2
            else:
                min=(min+max)/2
            if(max-min<0.01):
                break
        return min
    
    def hl( ls, inc, topf, botf ):
        Hlines=[]
        Vlines=[]
        i=-7
        incr=inc
        while(i<3.5):
            line = Line(start=topf.get_point_from_function(i), end=botf.get_point_from_function(i)).shift([1,0.8,0])
                    # Position the line at grid position

            
            line.set_stroke(WHITE, width=2)
            Hlines.append(line)
            i+=incr
        i=-7
        while(i<5.2):
            lft=-10
            rght=10
            if(i<botf.get_point_from_function(-7.11)[1]):
                lft=StokesVisual.functionbotmin(i, botf)
            else:
                lft=StokesVisual.functiontopmin(i, topf)
            if(i<botf.get_point_from_function(3.58)[1]):
                rght=StokesVisual.functionbotmax(i, botf)
            else:
                rght=StokesVisual.functiontopmax(i, topf)
            rght=min(rght, StokesVisual.functionbotmax(i, botf))
            line = Line(start=[lft, i,0], end=[rght, i,0]).shift([1,0.8,0])
                    # Position the line at grid position
        
            line.set_stroke(WHITE, width=2)
            Vlines.append(line)
            i+=incr
        ls=Hlines
        return ls
    
    def vl( ls, inc, topf, botf ):
        Hlines=[]
        Vlines=[]
        i=-7
        incr=inc
        while(i<3.5):
            line = Line(start=topf.get_point_from_function(i), end=botf.get_point_from_function(i)).shift([1,0.8,0])
                    # Position the line at grid position

            
            line.set_stroke(WHITE, width=2)
            Hlines.append(line)
            i+=incr
        i=-7
        while(i<5.2):
            lft=-10
            rght=10
            if(i<botf.get_point_from_function(-7.11)[1]):
                lft=StokesVisual.functionbotmin(i, botf)
            else:
                lft=StokesVisual.functiontopmin(i, topf)
            if(i<botf.get_point_from_function(3.58)[1]):
                rght=StokesVisual.functionbotmax(i, botf)
            else:
                rght=StokesVisual.functiontopmax(i, topf)
            rght=min(rght, StokesVisual.functionbotmax(i, botf))
            line = Line(start=[lft, i,0], end=[rght, i,0]).shift([1,0.8,0])
                    # Position the line at grid position
        
            line.set_stroke(WHITE, width=2)
            Vlines.append(line)
            i+=incr
        ls=Vlines
        return ls
    
        #self.play(LaggedStart(self.camera.frame.animate.shift([-1,0,0]), self.camera.frame.animate.set_width(5), lag_ratio=0.5, run_time=3 ) )
    def construct(self):
        # Create the curvy shape

        topf = FunctionGraph(
            lambda t: (3+0.06*math.pow(t-1,2)-0.2*math.fabs(t+1)*math.pow(math.e, math.pow(math.fabs(t+2),0.9) -3)),x_range=[-7.11,3.58],
            color=RED,
        ).shift([1, 0.8, 0])
        botf = FunctionGraph(
            lambda t: (-7+0.07*math.pow(t-1,2)+0.2*math.fabs(t+1)*math.pow(math.e, math.pow(math.fabs(t+2),0.9) -3)), x_range=[-7.11,3.58],
            color=RED,
        ).shift([1, 0.8, 0])
        self.add(topf, botf)
        Hlines=[]
        Vlines=[]
        i=-7
        incr=2.5
        while(i<3.5):
            line = Line(start=topf.get_point_from_function(i), end=botf.get_point_from_function(i)).shift([1,0.8,0])
                    # Position the line at grid position

            
            line.set_stroke(WHITE, width=2)
            Hlines.append(line)
            i+=incr
        i=-7
        incr=2.5
        while(i<5.2):
            lft=-10
            rght=10
            if(i<botf.get_point_from_function(-7.11)[1]):
                lft=StokesVisual.functionbotmin(i, botf)
            else:
                lft=StokesVisual.functiontopmin(i, topf)
            if(i<botf.get_point_from_function(3.58)[1]):
                rght=StokesVisual.functionbotmax(i, botf)
            else:
                rght=StokesVisual.functiontopmax(i, topf)
            rght=min(rght, StokesVisual.functionbotmax(i, botf))
            line = Line(start=[lft, i,0], end=[rght, i,0]).shift([1,0.8,0])
                    # Position the line at grid position
        
            line.set_stroke(WHITE, width=2)
            Vlines.append(line)
            i+=incr
        self.camera.frame.save_state()
        Hlines= StokesVisual.hl([], 2.5, topf, botf)
        Vlines= StokesVisual.vl([], 2.5, topf, botf)
        self.add(*Hlines, *Vlines)
        sq1=Square(2.5).shift([0.25,0.05,0]).set_color(color.BLUE_A)
        sq2=Square(2.5).shift([-2.25,0.05,0]).set_color(color.GREEN_E)
        txt=MathTex(r"\oint_C F \cdot \overrightarrow{dL}").set_color(color.WHITE).move_to([4,3,0])
        self.add(sq1, sq2)
        self.play(
            # Set the size with the width of a object
            self.camera.frame.animate.set_width(25)
            # Move the camera to the object
            #self.camera_frame.move_to,text
        )
        self.add(txt)
        self.play(Write(txt))
        self.play(self.camera.frame.animate.move_to([-1,0,0]).set(width=5), run_time=3)
        
        ArrB=Arrow(start=[-1,0,0], end=[-1.25, 0, 0], stroke_width=5).set_color(color.BLUE_C)
        ArrTxB=MathTex(r"\overrightarrow{dL}", font_size=15).set_color(color.BLUE_A)
        ArrG=Arrow(start=[-1,0,0], end=[-0.75, 0, 0], stroke_width=5).set_color(color.GREEN_D)
        ArrTxG=MathTex(r"\overrightarrow{dL}",  font_size=15).set_color(color.GREEN_E)
        ArrTxB.add_updater(lambda mob, dt: mob.set_x( (ArrB.get_x()) ) )
        ArrTxG.add_updater(lambda mob, dt: mob.set_x( (ArrG.get_x()) ) )
        ArrTxB.add_updater(lambda mob, dt: mob.set_y( (ArrB.get_y()+0.2) ) )
        ArrTxG.add_updater(lambda mob, dt: mob.set_y( (ArrG.get_y()+0.2) ) )



        self.add(ArrB,ArrTxB)
        self.play(Write(ArrB), Write(ArrTxB))
        self.play(Indicate(sq1, scale_factor=1.02, color=BLUE))
        self.play(ArrB.animate.shift([0,1,0]),  run_time=1.1)
        self.play(ArrB.animate.shift([0,-2,0]),  run_time=2.1)
        self.add(ArrG,ArrTxG)
        ArrG.shift([0,-1,0])  
        ArrTxG.shift([0,-1,0])
        self.play(Write(ArrG), Write(ArrTxG))
        self.play(Indicate(sq2, scale_factor=1.02, color=GREEN))
        self.play(ArrB.animate.shift([0,2,0]), ArrG.animate.shift([0,2,0]),  run_time=1.9)
        self.play(ArrB.animate.shift([0,-1,0]), ArrG.animate.shift([0,-1,0]),  run_time=1.0)
        rect=Rectangle(height=2.5, width=5).move_to([-1,0.05,0]).set_color(color.BLUE)
        self.play(Write(rect))
        self.play(self.camera.frame.animate.set_width(20), Unwrite(ArrB), Unwrite(ArrG), 
                  Unwrite(ArrTxB), Unwrite(ArrTxG), Unwrite(rect), Unwrite(sq1), Unwrite(sq2))
        Hlines=StokesVisual.hl([], 0.5, topf, botf)
        Vlines=StokesVisual.vl([], 0.5, topf, botf)
        self.add(*Hlines)
        self.add(*Vlines)
       
        grp=VGroup(*Hlines, *Vlines)
        self.play(Write(grp))
        sqs= dict()
        ls=[]
        for j in range(-12,10):
            topdog=0
            botdog=0
            
            
            for i in range(-12,10):
                sqs["{0}".format(i)+"{0}".format(j)]=Square(side_length=0.5).shift([i*0.5+0.25, j*0.5+0.55, 0])
                ls.append( Write (sqs["{0}".format(i)+"{0}".format(j)]) ) 
        ang= AnimationGroup(*ls)
        self.play(ang)

        




class ZAP(MovingCameraScene):
    def construct(self):
        # Add a background grid for reference
        grid = NumberPlane()
        self.add(grid)

        # Add a dot at the zoom target
        target_dot = Dot(point=RIGHT * 2 + UP * 1, color=RED)
        self.add(target_dot)

        # Initial wait
        self.wait(1)

        # Zoom and pan the camera frame
        self.play(
            self.camera.frame.animate.set(width=2).move_to(target_dot),
            run_time=3,
            rate_func=smooth
        )

        self.wait(1)