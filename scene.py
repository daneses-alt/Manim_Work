from cgi import print_arguments
from contextlib import nullcontext
import math
from manim import *
from sympy import false, mathematica_code
import manimpango

import numpy as np
from manim_fonts import *


def FLAG(size, x, y, self):

    rect1 = Rectangle(width=0.1, height=4)
    rect1.set_y(0)
    rect1.set_color(YELLOW)
    rect1.set_fill(YELLOW, opacity=0.99)

    p1 = np.array([0.05, 2, 0])
    p1b = p1 + [0.5, 0.2, 0]
    p2 = np.array([1.55, 1.6, 0])
    p2b = p2 - [0.4, 0.2, 0]

    bezier = CubicBezier(p1, p1b, p2b, p2)
    bezier.set_color(YELLOW)
    bezier2 = CubicBezier(p1 - [0, 0.75, 0], p1b - [0, 0.5, 0], p2b, p2)
    bezier.set_color(YELLOW)
    bezier2.set_color(YELLOW)
    circ = Circle(0.1)
    circ.set_color(YELLOW)
    circ.set_fill(YELLOW, opacity=1)
    circ.set_y(2.1)
    res = VGroup(bezier, bezier2, rect1, circ)
    #res.shift([0, 2, 0])
    res.shift([x,y,0])
    self.add(bezier, bezier2, rect1, circ)
    bezier.generate_target
    bezier2.generate_target
    allMobs = VGroup(*self.mobjects)
    allMobs.scale(size, about_point=[0, 0, 0])
    allMobs.shift([x, y, 0])
    p1 *= size
    p1b *= size
    p2 *= size
    p2b *= size
    p1 += [x, y, 0]
    p1b += [x, y, 0]
    p2 += [x, y, 0]
    p2b += [x, y, 0]
    lis = []
    for i in range(120):
        p2off = [0, size * math.sin(i / 5) / 5, 0]
        p1b = p1 + [size * 0.5, size * math.sin(1.2 + i / 5) / 3, 0]
        p2b = p2 + p2off - [size * 0.4, size * math.cos(i / 5) / 3, 0]
        bezier.target = CubicBezier(p1, p1b, p2b, p2 + p2off, color=YELLOW)
        bezier2.target = CubicBezier(
            p1 - [0, size * 0.75, 0],
            p1b - [0, size * 0.5, 0],
            p2b,
            p2 + p2off,
            color=YELLOW,
        )
        lis.append(MoveToTarget(bezier))
        lis.append(MoveToTarget(bezier2))
        self.play(MoveToTarget(bezier), MoveToTarget(bezier2), run_time=0.03)
    return lis
class FlagLoop(Scene):
    def construct(self):
        flag = FLAG(1.4, 0, 0, self)


# manim scene.py -pql Flag
def function(a, b):
        return math.e ** -(a ** 2 + b ** 2)+1

class ParaSurface(ThreeDScene):
    def func(self, u, v):
        return np.array([u, v, 1 + math.e ** (-u * u - v * v)])

    def func2(self, u, v):
        return np.array([u * np.sin(v), u * np.cos(v), (math.e + math.e ** (-(u * u)))])

    def construct(self):
        axes = ThreeDAxes(
            x_range=[-5, 5],
            x_length=10,
            y_range=[-5, 5],
            y_length=10,
            z_range=[-5, 5],
            z_length=10,
        )
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[-15, 15],
            v_range=[-15, 15],
            resolution=32,
            checkerboard_colors=([GREEN_B, GREEN_D]),
        )
        self.set_camera_orientation(theta=30 * DEGREES, phi=75 * DEGREES, zoom=1.4)
        sphr = Sphere(
            center=[3.6, 3, 1.1],
            radius=0.1,
            checkerboard_colors=False,
            fill_color=WHITE,
        )
        dx=0.0
        dy=0.0
        self.add(surface, sphr)
        vel = [-1.8, -1.6, 0]
        for i in range(15):
            x = sphr.get_x()
            y = sphr.get_y()
            dx = -2 * x * (math.e ** (-x * x - y * y))
            dy = -2 * y * (math.e ** (-x * x - y * y))
            vel[0] -= dx 
            vel[1] -= dy 
            vel[2]=function(x+vel[0]/5, y+vel[1]/5)-sphr.get_z()

            self.play(sphr.animate.shift([vel[0]/5, vel[1]/5, vel[2]]), rate_func=linear, run_time=0.2)

        # phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()
        self.wait()
        #self.play(distance_to_origin.animate.set_value(2))
        self.wait()


class CameraTest(ThreeDScene):
    def construct(self):
        phi, theta, focal_distance, gamma, distance_to_origin = (
            self.camera.get_value_trackers()
        )

        self.add(ThreeDAxes())
        self.wait()
        self.play(phi.animate.set_value(50 * DEGREES))
        self.play(theta.animate.set_value(50 * DEGREES))
        self.play(gamma.animate.set_value(1))
        self.play(distance_to_origin.animate.set_value(2))
        self.play(focal_distance.animate.set_value(25))
        self.wait()


class RotateAndColor(Rotate):
    def __init__(
        self,
        mobject: Mobject,
        angle: float,
        new_color,
        **kwargs,
    ) -> None:
        self.new_color = new_color
        super().__init__(mobject, angle=angle, **kwargs)

    def create_target(self) -> Mobject:
        target = self.mobject.copy()
        target.set_fill(self.new_color)
        target.set_color(self.new_color)
        target.rotate(
            self.angle,
            axis=self.axis,
            about_point=self.about_point,
            about_edge=self.about_edge,
        )
        return target


class FlagCircle(ThreeDScene):
    def construct(self):
        d = {}

        def mv(indcs, dist, dict, time):
            res = []
            for i in indcs:
                v = dict["flag{0}".format(i)]
                vect = (
                    np.array([v[2].get_x(), v[2].get_y(), 0])
                    / (math.sqrt(v[2].get_x() ** 2 + v[2].get_y() ** 2))
                    * dist
                )
                res.append(v.animate.shift(vect))
            ret = AnimationGroup(*res)
            ret.set_run_time(time)
            return ret
        flagstorot=Group
        for i in range(21):
            d["flag{0}".format(i)] = FLAG(1, 1, 1, self)
            d["flag{0}".format(i)].scale(0.3, about_point=ORIGIN)
            d["flag{0}".format(i)].shift(
                [
                    2 * math.cos(i * 2 * PI / 21 + PI / 2),
                    2 * math.sin(i * 2 * PI / 21 + PI / 2),
                    0,
                ]
            )
            d["flag{0}".format(i)].rotate(
                angle=i * 2 * PI / 21,
                about_point=(
                    d["flag{0}".format(i)][2].get_x(),
                    d["flag{0}".format(i)][2].get_y() - 0.6,
                    0,
                ),
            )
            self.add(d["flag{0}".format(i)])
            flagstorot.add(d["flag{0}".format(i)])
        
        background = Rectangle(height=20, width=20)
        background.set_fill(opacity=0.2)
        background.set_color([PINK, RED, LIGHT_PINK])
        self.add(background)

        #self.play(LaggedStart(mv([20], 7, d, 0.7)), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1)
        #self.play(LaggedStart(mv([0], 7, d, 0.7)), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1)
        #self.play(LaggedStart(mv([1], 7, d, 0.7)), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1)
        #self.play(Wait(0.6))
        #self.play(mv([20, 0, 1], -7, d, 1))
        self.play(mv([20], 7, d, 0.7))
        self.play(mv([20], -7, d, 0.7))   #2, 2, 2, 1, 1, 1, 1, 2, 3, 2, 3, 
        self.play(mv([20, 0], 7, d, 0.7))
        self.play(mv([20, 0], -7, d, 0.7))
        self.play(mv([20, 0, 1], 7, d, 0.7))
        self.play(mv([20, 0, 1], -7, d, 0.7))
        p1=Text(text="Player 1")
        p2=Text(text="Player 2")
        
        self.play(Rotate(Group(*self.mobjects), angle=-1 * PI / 21, about_point=ORIGIN))
        self.play(LaggedStart(mv([0, 1], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-2 * 2 * PI / 21, about_point=ORIGIN))
        self.play(LaggedStart(mv([2, 3], 7, d, 0.7), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-2 * 2 * PI / 21, about_point=ORIGIN))
        self.play(LaggedStart(mv([4, 5], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-1.5 * 2 * PI / 21, about_point=ORIGIN))
        self.play(LaggedStart(mv([6], 7, d, 0.7), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-1 * 2 * PI / 21, about_point=ORIGIN))
        self.play(LaggedStart(mv([7], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-1 * 2 * PI / 21, about_point=ORIGIN))
        self.play(LaggedStart(mv([8], 7, d, 0.7), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-1 * 2 * PI / 21, about_point=ORIGIN))
        self.play(LaggedStart(mv([9], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-1.5 * 2 * PI / 21, about_point=ORIGIN))
        self.play(LaggedStart(mv([10, 11], 7, d, 0.7), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-2.5 * 2 * PI / 21, about_point=ORIGIN))        
        self.play(LaggedStart(mv([12, 13, 14], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-2.5 * 2 * PI / 21, about_point=ORIGIN))       
        self.play(LaggedStart(mv([15, 16], 7, d, 0.7), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-2.5 * 2 * PI / 21, about_point=ORIGIN))       
        self.play(LaggedStart(mv([17, 18, 19], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))
        self.play(Rotate(Group(*self.mobjects), angle=-2 * 2 * PI / 21, about_point=ORIGIN))        
        self.play(LaggedStart(mv([20], 7, d, 0.7), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1))
        d2 = {}

        self.play(mv([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], -7, d, 0.7))
        img1=ImageMobject(filename_or_array="SadPink.png").scale(0.75)
        img2=ImageMobject(filename_or_array="HappyBlue.png").scale(0.75)
        self.add(img1, img2)
        img1.shift([-8, -1.7,0])
        img2.shift([-8, 1.7, 0])
        self.play(LaggedStart(img1.animate.shift([3, 0, 0]), img2.animate.shift([3, 0, 0]), lag_ratio=0, run_time=1))
        for i in range(5):
            d2["4clump{0}".format(i)] = VGroup(
                d["flag{0}".format(4 * i)],
                d["flag{0}".format(4 * i + 1)],
                d["flag{0}".format(4 * i + 2)],
                d["flag{0}".format(4 * i + 3)],
            )
        # self.play(d2["4clump{0}".format(3)].animate.set_fill(BLUE, opacity=1))
        self.play(
            d2["4clump{0}".format(0)].animate.set_color(RED_C),
            d2["4clump{0}".format(1)].animate.set_color(GREEN_C),
            d2["4clump{0}".format(2)].animate.set_color(BLUE_E),
            d2["4clump{0}".format(3)].animate.set_color(BLUE_A),
            d2["4clump{0}".format(4)].animate.set_color(PINK),
        )

        self.play(
            RotateAndColor(
                Group(*self.mobjects), 11 * 2 * PI / 21, GREEN, about_point=ORIGIN
            )
        )
        


class bunger2(ThreeDScene):
    def construct(self):
        d = {}
        def mv(indcs, dist, dict, time):
            res = []
            for i in indcs:
                v = dict["flag{0}".format(i)]
                vect = (
                    np.array([v[2].get_x(), v[2].get_y(), 0])
                    / (math.sqrt(v[2].get_x() ** 2 + v[2].get_y() ** 2))
                    * dist
                )
                res.append(v.animate.shift(vect))
            ret = AnimationGroup(*res)
            ret.set_run_time(time)
            return ret
        flagstorot=Group
        for i in range(21):
            d["flag{0}".format(i)] = FLAG(1, 1, 1, self)
            d["flag{0}".format(i)].scale(0.3, about_point=ORIGIN)
            d["flag{0}".format(i)].shift(
                [
                    2 * math.cos(i * 2 * PI / 21 + PI / 2),
                    2 * math.sin(i * 2 * PI / 21 + PI / 2),
                    0,
                ]
            )
            d["flag{0}".format(i)].rotate(
                angle=i * 2 * PI / 21,
                about_point=(
                    d["flag{0}".format(i)][2].get_x(),
                    d["flag{0}".format(i)][2].get_y() - 0.6,
                    0,
                ),
            )
            self.add(d["flag{0}".format(i)])
            flagstorot.add(d["flag{0}".format(i)])
        
        background = Rectangle(height=20, width=20)
        background.set_fill(opacity=0.2)
        background.set_color([PINK, RED, LIGHT_PINK])
        self.add(background)
        d2 = {}
        self.play(Rotate(Group(*self.mobjects), angle=2*PI/21, about_point=ORIGIN, run_time=0.1))
        for i in range(5):
            d2["4clump{0}".format(i)] = VGroup(
                d["flag{0}".format(4 * i)],
                d["flag{0}".format(4 * i + 1)],
                d["flag{0}".format(4 * i + 2)],
                d["flag{0}".format(4 * i + 3)],
            )
        # self.play(d2["4clump{0}".format(3)].animate.set_fill(BLUE, opacity=1))
        
        self.play(
            d2["4clump{0}".format(0)].animate.set_color(RED_C),
            d2["4clump{0}".format(1)].animate.set_color(GREEN_C),
            d2["4clump{0}".format(2)].animate.set_color(BLUE_E),
            d2["4clump{0}".format(3)].animate.set_color(BLUE_A),
            d2["4clump{0}".format(4)].animate.set_color(PINK), run_time=2
        )
        img1=ImageMobject(filename_or_array="HappyPink.png").scale(0.5).shift([-8, 0, 0])
        img2=ImageMobject(filename_or_array="HappyBlue.png").scale(0.5).shift([-6, 0, 0])
        self.add(img1, img2)
        

        self.play(LaggedStart(mv([20], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))

        self.play(LaggedStart(mv([0], 7, d, 0.7), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1))
        self.play(LaggedStart(mv([1,2,3], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))
        self.play(LaggedStart(mv([4,5], 7, d, 0.7), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1))
        self.play(LaggedStart(mv([6,7], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))
        self.play(LaggedStart(mv([8,9,10], 7, d, 0.7), background.animate.set_color([PINK, RED, LIGHT_PINK]), lag_ratio=0.7, run_time=1))
        self.play(LaggedStart(mv([11], 7, d, 0.7), background.animate.set_color([BLUE, BLUE_E, BLUE_B]), lag_ratio=0.7, run_time=1))
        self.play(LaggedStart(img2.animate.shift([-2, 0, 0]), img1.animate.shift([2, 0, 0]), lag_ratio=0.6))
        self.play(Wait(3))


class Nim(ThreeDScene):
    def construct(self):
        txt=Paragraph("Non-Constructive Proof: ", " ", "A proof that shows something exists (i.e. a winning strategy)", 
                      "without explicitly describing what that thing is.", font_size=30, line_spacing=0.7).shift([0, 3, 0])
        txt2=Paragraph("A proof that shows a winning strategy exists wihtout", 
                      "outlining what the strategy is.", font_size=30, line_spacing=0.7).shift([-0.7, -2, 0])
        ar = Arrow(color=ManimColor([200, 230, 230, 1]), stroke_width=3, )
        ar.set_angle(-PI / 2)
        ar.set_length(2)
        ar.set_y(0)
        ar.set_x(0)
        self.add(ar)
        ar.set_fill(ManimColor([200, 230, 230, 1]), opacity=1)
        img1=ImageMobject(filename_or_array="HappyPink.png").scale(0.3).shift([4, 0, 0])
        img2=ImageMobject(filename_or_array="HappyBlue.png").scale(0.3).shift([2, 0, 0])
        self.add(img1, img2)
        flg1=FLAG(1, 0, 0, self).scale(0.2, about_point=ORIGIN).shift([2.5, 0.15, 0])
        flg1.set_opacity(0)
        self.add(flg1)
        flg2=FLAG(1, 0, 0, self).scale(0.2, about_point=ORIGIN).shift([3, 0.15, 0])
        flg2.set_opacity(0)
        self.add(flg2)
        flg3=FLAG(1, 0, 0, self).scale(0.2, about_point=ORIGIN).shift([3.5, 0.15, 0])
        flg3.set_opacity(0)
        self.add(flg3)
        img1.set_opacity(0)
        img2.set_opacity(0)
        ar.set_opacity(0)
       
        self.play(Write(txt), run_time=2)
        self.play(Wait(2))
        self.play(img1.animate.set_opacity(1.0), img2.animate.set_opacity(1), ar.animate.set_opacity(1), flg1.animate.set_opacity(1.0), flg2.animate.set_opacity(1.0), 
                  flg3.animate.set_opacity(1.0))
        self.play(Wait(2))
        #flg1[1].aniamte.set_opacity(1), flg1[2].aniamte.set_opacity(1), flg1[3].aniamte.set_opacity(1))
        self.play(Write(txt2), run_time=2.0)
        self.play(Wait(2))

class NimSwap(ThreeDScene):
    def construct(self):
        def flag_update(mob):
            a=hlght.get_x() - mob.get_x()
            if a<0 and a>-1:
                mob.set_opacity(1+0.8*a)
            elif a<0:
                mob.set_opacity(0.2)

        t0 = MobjectTable([[Text("Alice", color=PINK)], [Text("Bob", color=BLUE)]]).move_to([-5.3, -2, 0]).scale(0.7)
        l1 = Line(start=[-5.3, -2, 0], end=[5, -2, 0])
        l2=Line(start=[-4.34, -1, 0], end=[-4.34, -3, 0])
        tab = VGroup(t0, l1)
        self.add(l1, t0, l2)
        dnums = {}
        flagd = {}
        for i in range(1, 10):
            flagd["flg{0}".format(i)] = FLAG(1, 1, 1, self).scale(0.3).move_to([-4.96 + i, 1, 0])
            c = flagd["flg{0}".format(i)].set_opacity(0)
            c.add_updater(flag_update)
            self.add(c)
        for i in range (1, 10):
            if(i%4==0):
                dnums["num{0}".format(i)]=Text(""+str(i), color=BLUE).scale(0.9).shift([-5+i, -2.5, 0])
            else:
                dnums["num{0}".format(i)]=Text(""+str(i), color=PINK).scale(0.9).shift([-5+i, -1.5, 0])
            a=dnums["num{0}".format(i)].set_opacity(0)
            self.add(a)
        hlght=Rectangle(color=WHITE, height=12, width=0.7).set_fill(WHITE).set_opacity(0).shift([4,0,0])
        self.add(hlght)
        txt1=Text("?", color=RED_D).move_to([3.2, -3, 0]).set_opacity(0)
        txt2=Text("?", color=RED_D).move_to([2.7, -2.9, 0]).scale(0.7).set_opacity(0)
        txt3=Text("?", color=RED_D).move_to([2.9, -2.2, 0]).scale(0.9).set_opacity(0)
        self.add(txt1, txt2, txt3)
        for mob in self.mobjects:
            mob.shift([0.5,0.5,0])
        for i in range (1, 9):
            self.play(LaggedStart(dnums["num{0}".format(i)].animate.set_opacity(1), flagd["flg{0}".format(i)].animate.set_opacity(1), lag_ratio=0.15))
        self.play(LaggedStart(hlght.animate.set_opacity(0.2), flagd["flg9"].animate.set_opacity(1), lag_ratio=0))
        self.play(dnums["num9"].animate.set_opacity(1))
        self.play(LaggedStart(hlght.animate.shift([-1,0,0])))
        self.play(Wait(1))
        self.play(txt1.animate.set_opacity(1), txt2.animate.set_opacity(1), txt3.animate.set_opacity(1))
        P2=Text("Player 2").move_to([t0.get_entries((2, 1)).get_x(), t0.get_entries((2, 1)).get_y(), 0]).scale(0.75)
        P1=Text("Player 1").move_to([t0.get_entries((1, 1)).get_x(), t0.get_entries((1, 1)).get_y(), 0]).scale(0.75)
        self.play(ReplacementTransform(t0.get_entries((2, 1)), P2) )
        self.play(Wait(1))
        self.play(ReplacementTransform(t0.get_entries((1, 1)), P1) )
        self.play(Wait(1))
        img1=ImageMobject(filename_or_array="HappyPink.png").scale(0.4).shift([-6.3, -0.8, 0])
        img2=ImageMobject(filename_or_array="HappyBlue.png").scale(0.4).shift([-6.3, -2.3, 0])
        self.add(img1, img2)
        self.play(Wait(1))
        self.play(hlght.animate.shift([1,0,0]), run_time=0.3)
        self.play(hlght.animate.shift([-1,0,0]), run_time=1)
        path=Circle(radius=0.75).move_to(img1.get_center()).shift([0, -0.75, 0]).set_opacity(0)
        self.add(path)
        #self.play(MoveAlongPath(img1, path, 0.5))
        self.play(Transform(img1,ImageMobject(filename_or_array="HappyPink.png").scale(0.4).shift([-6.3, -2.3, 0]), path_func=counterclockwise_path()))
        

        
       


class NimDemonstration(ThreeDScene):
    def construct(self):
        def modar(vg):
            vg.set_fill(opacity=1)
            vg.set_stroke(opacity=1)
            return vg

        def color_toggle(mob):
            if abs(ar.get_x() - mob.get_x()) < 2.5:
                a = abs(ar.get_x() - mob.get_x()) / 2.5
                mob.set_color(
                    ManimColor(
                        [
                            255 - 155 * (1 - a) * (1 - a),
                            255 - 225 * (1 - a) * (1 - a),
                            255 - 85 * (1 - a) * (1 - a),
                            1,
                        ]
                    )
                )
            else:
                mob.set_color(WHITE)

        def flag_update(mob):
            if ar.get_x() - mob.get_x() < -0.5:
                mob.set_color(GRAY)
                mob.set_fill(GRAY)
            else:
                mob.set_color(YELLOW)
                mob.set_fill(YELLOW)

        background = Rectangle(height=8.5, width=17)
        background.set_fill(opacity=0.3)
        background.set_color([TEAL, RED, YELLOW])
       
        self.add(background)
        t0 = MobjectTable([[Text("Alice", color=PINK)], [Text("Bob", color=BLUE)]]).move_to([-5, -2, 0]).scale(0.7)
        l1 = Line(start=[-5, -2, 0], end=[5, -2, 0])
        tab = VGroup(t0, l1)
        tab.stretch_about_point(0.1, 0, [-9, -2, 0])
        self.add(l1, t0)
        d = {}
        ar = Arrow(color=ManimColor([100, 30, 170, 1]), stroke_width=3)
        ar.set_angle(-PI / 2)
        ar.set_length(1)
        ar.set_y(3)
        ar.set_x(10)
        self.add(ar)
        ar.set_fill(ManimColor([100, 30, 170, 1]), opacity=1)
        numans = []
        flagd = {}
        nl = NumberLine(length=10, x_range=[0, 10]).move_to([-10, 2, 0])
        self.add(nl)
        for i in range(1, 11):
            flagd["flg{0}".format(i)] = (
                FLAG(1, 1, 1, self).scale(0.3).move_to([0, -9, 0])
            )
            c = flagd["flg{0}".format(i)]
            c.add_updater(flag_update)
            self.add(c)
        for i in range(1, 11):
            d["num{0}".format(i)] = Text(str(i)).move_to([0, 9, 0])
            c = d["num{0}".format(i)]
            c.generate_target
            c.target = Text(str(i)).move_to([i - 5, 2, 0])
            numans.append(MoveToTarget(c))
            numans.append(flagd["flg{0}".format(i)].animate.shift([i - 4.9, 9.7, 0]))
            c.add_updater(color_toggle)
            if i == 8:
                numans.append(tab.animate.stretch_about_point(10, 0, [-9, -1, 0]))
            self.add(c)
        self.play(
            LaggedStart(
                Circle(radius=0.3)
                .set_fill(opacity=1, color=RED)
                .move_to([0, 9, 0])
                .animate.shift([-5, -7, 0]),
                nl.animate.shift([10, 0, 0]),
                *numans,
                lag_ratio=0.15,
                run_time=1.8,
            )
        )

        self.play(ar.animate.move_to([-4, 3, 0]), run_time=0.6)
        self.play(ar.animate.shift([2, 0, 0]), run_time=0.6)
        self.play(ar.animate.shift([-2, 0, 0]), run_time=0.6)
        nbox = Square(side_length=0.6).move_to([-4, 2, 0])
        self.play(Write(nbox))
        # Wait(4)
        a1 = BraceLabel(
            text="1", obj=Square(side_length=1), brace_direction=UP
        ).move_to([-4.5, 2.7, 0])
        a1.set_fill(color=PINK, opacity=1)
        self.play(
            LaggedStart(
                ar.animate.shift([-1, 0, 0]), Create(a1), lag_ratio=0.4, run_time=1
            )
        )
        self.play(Wait(1))
        one=Integer(1).move_to([-4, -1.55, 0])
        self.add(one)
        one.set_fill(PINK, opacity=1)
        self.play(Create(one))
        self.play(
            LaggedStart(
                ar.animate.shift([2, 0, 0]),
                Uncreate(a1),
                nbox.animate.shift([1, 0, 0]),
                lag_ratio=0.4,
                run_time=1,
            )
        )

        a1 = BraceLabel(
            text="1", obj=Square(side_length=1), brace_direction=UP
        ).move_to([-3.5, 2.7, 0])
        a1.set_fill(color=PINK, opacity=1)
        b1 = BraceLabel(
            text="1", obj=Square(side_length=1), brace_direction=UP
        ).move_to([-4.5, 2.7, 0])
        b1.set_fill(color=BLUE, opacity=1)
        self.play(Wait(1))
        self.play(
            LaggedStart(
                ar.animate.shift([-1, 0, 0]), Create(a1), lag_ratio=0.4, run_time=1
            )
        )
        self.play(Wait(1))
        self.play(
            LaggedStart(
                ar.animate.shift([-1, 0, 0]), Create(b1), lag_ratio=0.4, run_time=1
            )
        )
        self.play(Wait(1))
        two=Integer(2).move_to([-3, -2.5, 0])
        self.add(two)
        two.set_fill(BLUE_C, opacity=1)
        self.play(Create(two))
        self.play(
            LaggedStart(
                ar.animate.shift([3, 0, 0]),
                Uncreate(b1),
                Uncreate(a1),
                nbox.animate.shift([1, 0, 0]),
                lag_ratio=0.4,
                run_time=1,
            )
        )

        a1 = BraceLabel(
            text="1", obj=Square(side_length=1), brace_direction=UP
        ).move_to([-2.5, 2.7, 0])
        a1.set_fill(color=PINK, opacity=1)
        b1 = BraceLabel(
            text="1", obj=Square(side_length=1), brace_direction=UP
        ).move_to([-3.5, 2.7, 0])
        b1.set_fill(color=BLUE, opacity=1)
        a2 = BraceLabel(
            text="1", obj=Square(side_length=1), brace_direction=UP
        ).move_to([-4.5, 2.7, 0])
        a2.set_fill(color=PINK, opacity=1)

        self.play(Wait(1))
        self.play(
            LaggedStart(
                ar.animate.shift([-1, 0, 0]), Create(a1), lag_ratio=0.4, run_time=1
            )
        )
        self.play(Wait(1))
        self.play(
            LaggedStart(
                ar.animate.shift([-1, 0, 0]), Create(b1), lag_ratio=0.4, run_time=1
            )
        )
        self.play(
            LaggedStart(
                ar.animate.shift([-1, 0, 0]), Create(a2), lag_ratio=0.4, run_time=1
            )
        )
        three=Integer(3).move_to([-2, -1.55, 0])
        self.add(three)
        three.set_fill(PINK, opacity=1)
        self.play(Create(three))
        self.play(
            LaggedStart(
                ar.animate.shift([4, 0, 0]),
                Uncreate(a2),
                Uncreate(b1),
                Uncreate(a1),
                nbox.animate.shift([1, 0, 0]),
                lag_ratio=0.4,
                run_time=1,
            )
        )

        A1 = BraceLabel(text="4", obj=Square(side_length=4), brace_direction=UP).move_to([-3, 2.7, 0])
        A1.set_fill(color=PINK, opacity=1)
        self.play(Wait(1))
        self.play(
            LaggedStart(
                ar.animate.shift([-4, 0, 0]), Create(A1), lag_ratio=0.4, run_time=1
            )
        )
        self.play(Wait(1))
        four=Integer(4).move_to([-1, -1.55, 0])
        self.add(four)
        four.set_fill(PINK, opacity=1)
        self.play(Create(four))
        self.play(Wait(1))


class putnam(ThreeDScene):
    def construct(self):
        t0 = Table([["Alice"], ["Bob"]]).move_to([-5, -2, 0]).scale(0.7)
        l1 = Line(start=[-5, -2, 0], end=[5, -2, 0])
        tab = VGroup(t0, l1)
        self.add(l1, t0)
        d = {}
        flagd = {}
        nl = NumberLine(length=10, x_range=[0, 10]).move_to([0, 1, 0])
        self.add(nl)
        for i in range(1, 11):
            flagd["flg{0}".format(i)] = (
                FLAG(1, 1, 1, self).scale(0.3).move_to([-5.5 + i, 0, 0])
            )
            c = flagd["flg{0}".format(i)]
            self.add(c)
        for i in range(1, 11):
            d["num{0}".format(i)] = Text(str(i)).move_to([-5.5 + i, 2, 0])
            c = d["num{0}".format(i)]
            c.generate_target
            c.target = Text(str(i)).move_to([i - 5, 2, 0])
            MoveToTarget(c)
            self.add(c)
        self.play(Wait(3))
        X = (
            Text(
                str("X"),
                stroke_width=0,
                color=RED_E,
                font="arial",
                fill_opacity=0,
                tab_width=5,
            )
            .stretch_about_point(25, 0, [0, 0, 0])
            .stretch_about_point(15, 1, [0, 0, 0])
        )
        self.add(X)
        self.play(X.animate.set_fill(color=RED_E, opacity=1))
        self.play(Wait(1))
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
        )
        heading = Text(str("Proof By Contradiction"), color=WHITE).move_to([0, 5, 0])
        self.play(
            LaggedStart(
                heading.animate.move_to([0, 3, 0]),
                Create(Underline(heading).shift([0, -2, 0])),
                lag_ratio=0.8,
                run_time=0.9,
            )
        )


class putnam2(ThreeDScene):
    def construct(self):
        clm = Tex(str("Bob wins for infinitely many n")).move_to(
            [-2, 2, 0]
        )
        opp1 = Tex(str("Bob wins for")).move_to([-3.9, 2, 0])
        opp2 = Tex(str("infinitely many n")).next_to(
            opp1, RIGHT, buff=0.2
        ).shift([0,-0.05,0])
        self.add(clm)
        self.play(Write(clm), run_time=2)
        self.add(opp1, opp2)
        self.play(opp1.animate.shift([0, -1, 0]), opp2.animate.shift([0, -1, 0]))
        opp1p=opp1.copy()
        co1=Tex(str("Bob wins for")).move_to([-3.9,1,0])
        co1[0][4:6].set_color(RED)
        co2=Tex(str("infinitely many n")).next_to(
            opp1, RIGHT, buff=0.2
        ).shift([0,-0.05,0])
        co2[0][0:2].set_color(RED)
        self.play(AnimationGroup(Transform(opp1, co1)))
        self.play(Transform(co1, opp1p))
        self.play(Transform(opp2, co2))
        self.remove(opp2, opp1)
        self.play(Transform(co2, Tex(str("finitely many n")).next_to(
            opp1p, RIGHT, buff=0.2
        ).shift([0,-0.05,0])))
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{ragged2e}")
        self.play(Write(Tex(r"$\Longleftrightarrow$ There exists a maximal value of $n$ for \newline which Bob can win.", tex_template=myTemplate, tex_environment="justify").move_to([-0.7,-0.3,0])))
        self.play(Wait(2))
        self.play(Write(Tex(r"We will call this maximal value $M$").move_to([-1.6, -1.6, 0])))
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class putnam3(ThreeDScene):
    def construct(self):
        t0 = MobjectTable([[Text("Alice", color=PINK), Tex(""), Tex("$M+1$", color=PINK).scale(1.3), Tex("$M+2$", color=PINK).scale(1.3), Tex("..."), Tex("$n$", color=PINK).scale(1.3), Tex("$n+1 ...$", color=PINK).scale(1.3)], 
                           [Text("Bob", color=BLUE), Tex("$ M $", color=BLUE).scale(1.3), Tex(""), Tex(""), Tex("..."), Tex(""), Tex("  ...")]],
                           include_outer_lines=True).move_to([-1, 3, 0]).scale(0.7)
        t0.get_cell([2,2]).set_color(GREEN)
        self.add(t0)
        self.play(LaggedStart(Create(t0.get_cell([2,2]).set_color(GREEN))))
        self.play(LaggedStart(Create(t0.get_cell([2,2]).set_color(WHITE)), Create(t0.get_cell([1,3]).set_color(GREEN)), lag_ratio=0.5))
        self.play(LaggedStart(Create(t0.get_cell([1,3]).set_color(WHITE)), Create(t0.get_cell([1,4]).set_color(GREEN)), lag_ratio=0.5))
        d={}
        for i in range(1,11):
            d["flag{0}".format(i)]=FLAG(0.2, 0, 0, self).shift([-7.5+i/2.0, -5, 0]).scale(0.27)
            self.add(d["flag{0}".format(i)])
        self.add(Text(". . .").next_to(d["flag{0}".format(10)], RIGHT, buff=0.5))
        self.play(Wait(3))

class Count(Animation):
    def __init__(self, number: Integer, start: Integer, end: Integer, **kwargs) -> None:
        super().__init__(number,  **kwargs)
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        self.mobject.set_value(self.start - (alpha * (0.5+self.start - self.end)))
        if self.mobject.get_value()==9:
            self.mobject.move_to([6.03,-3,0])

class scenetrans(Scene):
    def construct(self):
        back=Rectangle(height=10, width=15.22)
        back2=Rectangle(height=10, width=15.22)
        back.set_opacity(0.5)
        back2.set_opacity(0.2)
        back.set_color([TEAL_D, LIGHT_PINK, PURE_GREEN])
        back2.set_color([TEAL, BLUE, GREEN_A])
        slider=Polygon([-13, -4, 0], [8, -4, 0], [13, 4, 0], [-8, 4, 0], stroke_width=0).shift([-20,0,0]).set_fill(BLACK, opacity=0.9)
        self.add(back)
        self.add(back2)
        self.add(slider)
        timer=Integer(20).move_to([6,-3,0])
        self.add_foreground_mobject(timer)
        self.play(slider.animate.shift([18,0,0]), Count(timer, 20, 0), run_time=20, rate_func=linear)
        
class scenetransimage(Scene):
    def construct(self):
    
        with RegisterFont("Quattrocento") as fnts:
            a = Text("Hint #1", font=fnts[0], weight=BOLD, color=BLUE_C).move_to([-3.2, 3, 0]).scale(1)
            text3 = Text("Hint #2", font=fnts[0], weight=BOLD, color=BLUE_C).move_to([3.2, 3, 0]).scale(1)
            parag2= Paragraph( '\t\t\t\tThink about', '\"complementary moves\" in', 'this problem and what they', 'sum to.',                 
                          line_spacing=0.7, font=fnts[0]).move_to([3.2,1.5,0]).scale(0.5)
            parag3 = Paragraph( '\t\t\tWork your way up!', 'Determine who wins if there', 'is initially 1 flag, 2 flags, 3 flags …', 'and try to build to 20.',
                                line_spacing=0.7, font=fnts[0]).move_to([-3.1,1.4,0]).scale(0.5) 
            self.play(Write(a))
            self.play(Wait(1))
            self.play(Write(parag3))
            self.play(Wait(1))
            self.play(Write(text3))
            self.play(Wait(1))
            self.play(Write(parag2))
            self.play(Wait(20))

def justify(s: str, max: Integer) -> list[str]:
    res=[]
    ls=s.split()
    ind=0
    curr=""
    while ind<ls.__len__():
        while ind<ls.__len__() and (curr.__len__()==0 or curr.__len__()+ls[ind].__len__()<max):
            curr+=ls[ind]+" "
            ind+=1
        res.append(curr)
        curr=""
        if ind<ls.__len__():
            curr=ls[ind]+" "
        ind+=1
    return res


class AllFonts1(Scene):
    def construct(self):
        fsize = 44
        fonts = manimpango.list_fonts()
        i=0
        for f in fonts:
           self.add(Text(f, font =f, color=BLUE).move_to([-5+i%20, 3-math.floor(i/20), 0]))
           i+=4


class Example(Scene):
    def construct(self):
         self.add(ImageMobject(r"scenetransimage_ManimCE_v0.18.1.png"))
         for i in range(1, 40):
            img = ImageMobject(r"tra_frm"+str(i)+".png")
            self.add(img)
            self.play(Wait(2/17))
            self.remove(img)

class pigolf(Scene):
    def construct(self):
        s=list


class scenetransimage2(Scene):
    def construct(self):
    
        with RegisterFont("Quattrocento") as fnts:
            a = Text("Hint #1", font=fnts[0], weight=BOLD, color=BLUE_C).move_to([-3.2, 3, 0]).scale(1)
            text3 = Text("Hint #2", font=fnts[0], weight=BOLD, color=BLUE_C).move_to([3.2, 3, 0]).scale(1)
            parag2= Paragraph( '\t\t\tConsider the flags as', '5 groups of 4, as well as the one', 'remaining flag (i.e., the 21st flag).', 'Think about the problem in terms', 'of groups of 4 flags being removed.',                 
                          line_spacing=0.7, font=fnts[0]).move_to([3.3,1.2,0]).scale(0.5)
            parag3 = Paragraph( '\t\t\tWork your way up!', 'Determine who wins if there is', 'initially 1 flag, 2 flags, 3 flags …', 'and try to build to 20.',
                                line_spacing=0.7, font=fnts[0]).move_to([-3.1,1.4,0]).scale(0.5) 
            self.play(Write(a))
            self.play(Wait(1))
            self.play(Write(parag3))
            self.play(Wait(1))
            self.play(Write(text3))
            self.play(Wait(1))
            self.play(Write(parag2))
            self.play(Wait(20))


#class NimFund(Scene):
 #   def construct(self):



