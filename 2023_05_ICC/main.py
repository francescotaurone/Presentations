from manim import *
from manim_slides import Slide
import os
sys.path.insert(0, os.path.abspath(".."))
import samplingUtils as su
import numpy as np

class SubclassExample(Slide, MovingCameraScene):
    def construct(self):
        eq1 = MathTex(r"x = 1")
        eq2 = MathTex(r"x = 2")
        self.play(Write(eq1))
        self.next_slide()
        self.play(TransformMatchingTex(eq1, eq2),
            self.camera.frame.animate.scale(1.5)
        )
        self.wait()

class FullPresentation(MovingCameraScene):
    #config["frame_rate"] = 6
    def construct(self):       
        self.next_section(skip_animations=False)     
        def place_at_the_top_of_frame(mobj):
            mobj.move_to(self.camera.frame_center + UP*(self.camera.frame_height/2)*0.88 )
            mobj.rescale_to_fit(self.camera.frame_width*0.8, 0)
            mobj.underline.set_stroke(width = self.camera.frame_height/10)
        def write_exponent_bit_value_n1(mobj):
            x_fp_exp = su.getFPUnbiasedExponent32bits(self.x_fp.get_value())
            exp_bin = bin(x_fp_exp)[2:].rjust(8, "0")
            #mobj.become(MathTex(f"{x_fp_exp % (2**(mobj.index+1))}"))
            mobj.set_value(int(exp_bin[mobj.index]))
        def write_exponent_bit_value_n2(mobj):
            y_fp_exp = su.getFPUnbiasedExponent32bits(self.y_fp.get_value())
            exp_bin = bin(y_fp_exp)[2:].rjust(8, "0")
            mobj.set_value(int(exp_bin[mobj.index]))
        def write_mantissa_bit_value_x_fp(mobj):
            x_fp_mantissa = su.getLongIntFromSingleMantissa(self.x_fp.get_value())
            mantissa_bin = bin(x_fp_mantissa)[2:].rjust(23, "0")
            mobj.set_value(int(mantissa_bin[mobj.index-1]))
        def write_mantissa_bit_value_y_fp(mobj):
            y_fp_mantissa = su.getLongIntFromSingleMantissa(self.y_fp.get_value())
            mantissa_bin = bin(y_fp_mantissa)[2:].rjust(23, "0")
            mobj.set_value(int(mantissa_bin[mobj.index-1]))
        def place_dot_x_fp(mobj):
            mobj.move_to(self.real_line.n2p(self.x_fp.get_value()))
        def place_dot_y_fp(mobj):
            mobj.move_to(self.real_line.n2p(self.y_fp.get_value()))
        self.camera.frame.save_state() 
        self.camera.background_color = "#edf2f4"
        color_list = [ RED, "#E3B505", "#654F6F", "#107E7D", "#FF784F",]
        Text.set_default(color=BLACK)
        BraceBetweenPoints.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        DashedLine.set_default(color=BLACK)
        Dot.set_default(color=BLACK)
        DoubleArrow.set_default(max_tip_length_to_length_ratio=0.5)
        title_of_the_paper = Title(
            f"Change a Bit to save Bytes: Compression for Floating Point Time-Series Data,\
            F. Taurone, D. E. Lucani, M. Fehér, Q. Zhang -  Aarhus University, Denmark",
            stroke_color = BLACK, font_size = 35, underline_buff=SMALL_BUFF).add_updater(place_at_the_top_of_frame)
        title_of_the_paper.underline.set_color(BLACK)
        self.add(title_of_the_paper) 
        
###########
# COMPRESSION
###########

        shared_sequence = "100010111"
        line1 = MathTex(r"1010010", r"{{{}}}".format(shared_sequence))
        line2 = MathTex(r"0001001", r"{{{}}}".format(shared_sequence))
        line3 = MathTex(r"0010111", r"{{{}}}".format(shared_sequence))
        line4 = MathTex(r"1010011", r"{{{}}}".format(shared_sequence))
        line5 = MathTex(r"1111100", r"{{{}}}".format(shared_sequence))
        line6 = MathTex(r"0001100", r"{{{}}}".format(shared_sequence))
        lines = VGroup(
            line1, line2, line3,
            line4, line5, line6,
        )
        lines.arrange(direction=DOWN, buff=0.1)
        self.add(*lines.submobjects)
        frame = Rectangle(
            width = lines.width + SMALL_BUFF,
            height = lines.height+ SMALL_BUFF,
            color = BLACK
        ).move_to(
            lines.get_center()
        )
        self.add(frame)
        #self.camera.frame.set(width=line1.width * 1.2)
        self.camera.frame.scale(0.5)
        self.play(
            #self.camera.frame.animate.scale(0.5)
            AnimationGroup(*[
                FadeToColor(line[1], RED)#[-len(shared_sequence):], RED)
                    for line in lines
                ]
            ),
        )
        self.wait()
        last_line = MathTex(
            r"\star = {{{}}}".format(shared_sequence),
            color = RED
        ).next_to(
            line6, DOWN , buff=0.1
        ).align_to(
            line6,LEFT 
        )

        transformed_lines = [
            MathTex(
                    r"1010010", r"\star"
            ),
            MathTex(
                    r"0001001", r"\star"
            ),
            MathTex(
                    r"0010111", r"\star"
            ),
            MathTex(
                    r"1010011", r"\star"
            ),
            MathTex(
                    r"1111100", r"\star"
            ),
            MathTex(
                    r"0001100", r"\star"
            ),
        ]
        transformed_lines_vg = VGroup(*transformed_lines)

        for line in transformed_lines:
            line[1].set(color = RED)
        self.play(
            Write(last_line),
            TransformMatchingTex(
                line1, transformed_lines[0].move_to(line1.get_center()).align_to(line1, LEFT)
            ),
            TransformMatchingTex(
                line2, transformed_lines[1].move_to(line2.get_center()).align_to(line2, LEFT)
            ),
            TransformMatchingTex(
                line3, transformed_lines[2].move_to(line3.get_center()).align_to(line3, LEFT)
            ),
            TransformMatchingTex(
                line4, transformed_lines[3].move_to(line4.get_center()).align_to(line4, LEFT)
            ),
            TransformMatchingTex(
                line5, transformed_lines[4].move_to(line5.get_center()).align_to(line5, LEFT)
            ),
            TransformMatchingTex(
                line6, transformed_lines[5].move_to(line6.get_center()).align_to(line6, LEFT)
            )
        )
        self.wait()
        self.play(
            Transform(
                frame, 
                Rectangle(
                    width = transformed_lines_vg.width + SMALL_BUFF,
                    height = transformed_lines_vg.height+ SMALL_BUFF,
                    color = BLACK
                ).move_to(
                    transformed_lines_vg.get_center()
                )
            ),
            Write(
                Rectangle(
                    width = last_line.width + SMALL_BUFF,
                    height = last_line.height+ SMALL_BUFF,
                    color = RED
                ).move_to(
                    last_line.get_center()
                )
            )
        ) 
        #self.camera.auto_zoom(mobjects = lines.submobjects, animate = False)
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title_of_the_paper]
            # All mobjects in the screen are saved in self.mobjects
        )
        self.play(
            Restore(self.camera.frame)
        )
        self.wait()

###########
# ADDITION
###########
        x_power_min = 8
        x_power_max = 8
        negative_powers_list = list(range(x_power_min+1, 0, -1))
        positive_power_list = list(range(-1, x_power_max+1))
        lab1 = [MathTex(r"-2^{{{}}}".format(power)) for power in negative_powers_list]
        lab2 = [MathTex(r"0")]
        lab3 = [MathTex(r"2^{{{}}}".format(power)) for power in positive_power_list]
        x_labels = [*lab1, *lab2, *lab3]
        self.real_line = NumberLine(
            x_range=[-2**x_power_min, 2**x_power_max, 0.5],
            length=52*config.frame_width,
            color=WHITE,
            include_numbers=False,
            label_direction=UP,
            include_tip=True,
            stroke_color = BLACK
            #numbers_to_include = x_values,
            #decimal_number_config = {"num_decimal_places": 0},
        )
        self.play(Write(self.real_line))
        for i in range(len(lab1)):
            lab1[i].power = negative_powers_list[i]
            lab1[i].add_updater(
                update_function = 
                    lambda mobj: mobj.move_to(
                    self.real_line.n2p(-2.0**mobj.power) + UP*0.5
                    ),
                call_updater = True
            )
        for i in range(len(lab2)):
            lab2[i].power = 0
            lab2[i].add_updater(
                update_function = 
                    lambda mobj: mobj.move_to(
                    self.real_line.n2p(0) + UP*0.5
                    ),
                call_updater = True
            )
        for i in range(len(lab3)):
            lab3[i].power = positive_power_list[i]
            lab3[i].add_updater(
                update_function = 
                    lambda mobj: mobj.move_to(
                    self.real_line.n2p(2.0**mobj.power) + UP*0.5
                    ),
                call_updater = True
            )
        
        self.play(AnimationGroup(*[Write(label) for label in x_labels]))
        self.wait()
        brace1 = BraceBetweenPoints(self.real_line.n2p(0.5),self.real_line.n2p(1.0), direction=UP, buff = 1.0)
        brace1_text = Tex("$2^{23}$ numbers").next_to(brace1, UP)
        brace2 = BraceBetweenPoints(self.real_line.n2p(1),self.real_line.n2p(2), direction=DOWN, buff = 0.2)
        brace2_text = Tex("$2^{23}$ numbers").next_to(brace2, DOWN)
        brace3 = BraceBetweenPoints(self.real_line.n2p(2),self.real_line.n2p(4), direction=UP, buff =1.0)
        brace3_text = Tex("$2^{23}$ numbers").next_to(brace3, UP)
        brace4 = BraceBetweenPoints(self.real_line.n2p(4),self.real_line.n2p(8), direction=UP, buff =1.0)
        brace4_text = Tex("$2^{23}$ numbers").next_to(brace4, UP)
        brace5 = BraceBetweenPoints(self.real_line.n2p(8),self.real_line.n2p(16), direction=UP, buff =1.0)
        brace5_text = Tex("$2^{23}$ numbers").next_to(brace5, UP)
        braces = [brace1, brace2, brace3, brace4, brace5]
        braces_text = [brace1_text, brace2_text, brace3_text, brace4_text, brace5_text]
        real_line_vg = VGroup(self.real_line,
                              brace1, brace1_text,
                              brace2, brace2_text,
                              brace3, brace3_text,
                              brace4, brace4_text,
                              brace5, brace5_text,
        )
        self.play(FadeIn(brace1), FadeIn(brace1_text),
                  FadeIn(brace2), FadeIn(brace2_text),
                  FadeIn(brace3), FadeIn(brace3_text),
                  FadeIn(brace4), FadeIn(brace4_text),
                  FadeIn(brace5), FadeIn(brace5_text),
        )

        self.wait()
        
        self.play(self.camera.frame.animate.scale(1.5),    
        )

        self.play(real_line_vg.animate.shift(2.72*UP))
        self.wait()
        ## X DEFINITION
        self.x_fp = ValueTracker(5.39)
        self.y_fp = ValueTracker(15.12)
        x_fp_exp2 = Dot(self.real_line.n2p(self.x_fp.get_value()))
        x_fp_exp2.add_updater(place_dot_x_fp)
        x_fp_exp3 = Dot(self.real_line.n2p(self.y_fp.get_value()))
        x_fp_exp3.add_updater(place_dot_y_fp)
        x_fp_exp2_label = MathTex(r"{{x}}").next_to(x_fp_exp2, DOWN)
        x_fp_exp3_label = MathTex(r"{{x}}_2").next_to(x_fp_exp3, DOWN)
        self.play(Indicate(x_fp_exp2), Indicate(x_fp_exp2_label), 
                  #Indicate(x_fp_exp3), Indicate(x_fp_exp3_label)
        )
        self.wait()
        fp_formula = MathTex(r"{{x}} = (-1)^S \cdot 2^{E-127}\cdot\left(2^{23} + \sum_{i = 1}^{23}m_i \cdot 2^{23-i}\right)").move_to(self.camera.frame_center)
        fp_formula_onedot = MathTex(r"{{x}} = (-1)^S \cdot 2^{E-127}\cdot\left(1.m_1m_2\dotsm m_{23}\right)"
                            ).move_to(self.camera.frame_center)
        fp_formula_forx_exp2 = MathTex(r"{{x}}{{ = 2^{ {2} }\cdot\left(1.}}{{m_1}}{{m_2}}{{\dotsm m_{23}\right)}}",
                            ).next_to(self.real_line.n2p(6), DOWN, buff = 1.0)
        fp_formula_forx_exp3 = MathTex(r"{{x}}{{ = 2^{ {3} }\cdot\left(1.}}{{m_1}}{{m_2}}{{\dotsm m_{23}\right)}}",
                             ).next_to(self.real_line.n2p(12), DOWN, buff=1.0)
        #self.play(Write(fp_formula))
        
        #self.add(index_labels(fp_formula_forx_exp2[0]))
        fp_formula_forx_exp2[1][2].set_color(color_list[0])
        fp_formula_forx_exp2.set_color_by_tex("m_1", color_list[1])
        fp_formula_forx_exp2.set_color_by_tex("m_2", color_list[2])
        fp_formula_forx_exp3[1][2].set_color(color_list[0])
        fp_formula_forx_exp3.set_color_by_tex("m_1", color_list[1])
        fp_formula_forx_exp3.set_color_by_tex("m_2", color_list[2])
        self.play(TransformMatchingTex(x_fp_exp2_label, fp_formula),
                   #TransformMatchingTex(x_fp_exp3_label, fp_formula)
        )
        self.wait()
        self.play(TransformMatchingTex(fp_formula, fp_formula_onedot))
        self.wait()
        self.play(TransformMatchingTex(fp_formula_onedot.copy(), fp_formula_forx_exp2),
                   TransformMatchingTex(fp_formula_onedot, fp_formula_forx_exp3) )
        ## mantissa boundary
        boundary_length = 8 
        p4 = self.real_line.n2p(4)
        p8 = self.real_line.n2p(8)
        p16 = self.real_line.n2p(16)
        four_boundary= DashedLine(p4, p4 + boundary_length*DOWN, color = RED) 
        eight_boundary= DashedLine(p8, p8 + boundary_length*DOWN, color = RED) 
        sixteen_boundary= DashedLine(p16, p16 + boundary_length*DOWN, color = RED) 

        self.play(Write(four_boundary),
                  Write(eight_boundary),
                  Write(sixteen_boundary),
        )
        self.wait()
        
        vertical_shift = 1

        ## Exponent Arrow
        exp_arr_pow2 = DoubleArrow(p4+ vertical_shift*DOWN, p8+vertical_shift*DOWN, buff=0, color=color_list[0])
        exp_arr_pow2_gv =  VGroup(exp_arr_pow2, MathTex(r"E_U = 2", color = color_list[0]).next_to(exp_arr_pow2, UP, buff = 0.1))
        exp_arr_pow3 = DoubleArrow(p8 +vertical_shift*DOWN, p16+vertical_shift*DOWN, buff=0, color=color_list[0])
        exp_arr_pow3_gv = VGroup(exp_arr_pow3, MathTex(r"E_U = 3", color = color_list[0]).next_to(exp_arr_pow3, UP, buff = 0.1))

        self.play(
            fp_formula_forx_exp2.animate.shift(DOWN),
            fp_formula_forx_exp3.animate.shift(DOWN),
            FadeIn(exp_arr_pow2_gv),
            FadeIn(exp_arr_pow3_gv),
        )
        self.wait()

        ## m1 Arrow
        p6 = self.real_line.n2p(6)
        p12 = self.real_line.n2p(12)
        m1_arr_pow2_1 = DoubleArrow(p4+ 2*vertical_shift*DOWN, p6+2*vertical_shift*DOWN, buff=0, color=color_list[1])
        m1_arr_pow2_2 = DoubleArrow(p6+ 2*vertical_shift*DOWN, p8+2*vertical_shift*DOWN, buff=0, color=color_list[1])
        m1_arr_pow2_gv =  VGroup(
            m1_arr_pow2_1,
            m1_arr_pow2_2,
            MathTex(r"m_1 = 0", color = color_list[1]).next_to(m1_arr_pow2_1, UP, buff = 0.1),
            MathTex(r"m_1 = 1", color = color_list[1]).next_to(m1_arr_pow2_2, UP, buff = 0.1),
        )
        m1_arr_pow3_1 = DoubleArrow(p8 +2*vertical_shift*DOWN, p12+2*vertical_shift*DOWN, buff=0, color=color_list[1])
        m1_arr_pow3_2 = DoubleArrow(p12 +2*vertical_shift*DOWN, p16+2*vertical_shift*DOWN, buff=0, color=color_list[1])
        m1_arr_pow3_gv = VGroup(
            m1_arr_pow3_1,
            m1_arr_pow3_2,
            MathTex(r"m_1 = 0", color = color_list[1]).next_to(m1_arr_pow3_1, UP, buff = 0.1),
            MathTex(r"m_1 = 1", color = color_list[1]).next_to(m1_arr_pow3_2, UP, buff = 0.1),
        )

        self.play(
            fp_formula_forx_exp2.animate.shift(DOWN),
            fp_formula_forx_exp3.animate.shift(DOWN),
            FadeIn(m1_arr_pow2_gv),
            FadeIn(m1_arr_pow3_gv ),
        )
        self.wait()

        ## m2 Arrow
        p5 = self.real_line.n2p(5)
        p7 = self.real_line.n2p(7)
        p10 = self.real_line.n2p(10)
        p14 = self.real_line.n2p(14)
        m2_arr_pow2_1 = DoubleArrow(p4+ 3*vertical_shift*DOWN, p5+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow2_2 = DoubleArrow(p5+ 3*vertical_shift*DOWN, p6+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow2_3 = DoubleArrow(p6+ 3*vertical_shift*DOWN, p7+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow2_4 = DoubleArrow(p7+ 3*vertical_shift*DOWN, p8+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        
        m2_arr_pow2_gv =  VGroup(
            m2_arr_pow2_1,
            m2_arr_pow2_2,
            m2_arr_pow2_3,
            m2_arr_pow2_4,
            MathTex(r"m_2 = 0", color = color_list[2], font_size=40).next_to(m2_arr_pow2_1, UP, buff = 0.1),
            MathTex(r"m_2 = 1", color = color_list[2], font_size=40).next_to(m2_arr_pow2_2, UP, buff = 0.1),
            MathTex(r"m_2 = 0", color = color_list[2], font_size=40).next_to(m2_arr_pow2_3, UP, buff = 0.1),
            MathTex(r"m_2 = 1", color = color_list[2], font_size=40).next_to(m2_arr_pow2_4, UP, buff = 0.1),
        )

        m2_arr_pow3_1 = DoubleArrow(p8 +3*vertical_shift*DOWN, p10+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow3_2 = DoubleArrow(p10 +3*vertical_shift*DOWN, p12+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow3_3 = DoubleArrow(p12 +3*vertical_shift*DOWN, p14+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow3_4 = DoubleArrow(p14 +3*vertical_shift*DOWN, p16+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        
        m2_arr_pow3_gv = VGroup(
            m2_arr_pow3_1,
            m2_arr_pow3_2,
            m2_arr_pow3_3,
            m2_arr_pow3_4,
            MathTex(r"m_2 = 0", color = color_list[2], font_size=40).next_to(m2_arr_pow3_1, UP, buff = 0.1),
            MathTex(r"m_2 = 1", color = color_list[2], font_size=40).next_to(m2_arr_pow3_2, UP, buff = 0.1),
            MathTex(r"m_2 = 0", color = color_list[2], font_size=40).next_to(m2_arr_pow3_3, UP, buff = 0.1),
            MathTex(r"m_2 = 1", color = color_list[2], font_size=40).next_to(m2_arr_pow3_4, UP, buff = 0.1),
        )

        self.play(
            fp_formula_forx_exp2.animate.shift(DOWN),
            fp_formula_forx_exp3.animate.shift(DOWN),
            FadeIn(m2_arr_pow2_gv),
            FadeIn(m2_arr_pow3_gv ),
        )
        self.wait()
        #dots
        dots_pow2 = VGroup(
            *[
                Dot(p6 + 4*vertical_shift*DOWN + i*0.2*DOWN)
                for i in range(3)
            ]
        )
        dots_pow2_anim = [FadeIn(dot, shift=DOWN) for dot in dots_pow2]

        dots_pow3 = VGroup(
            *[
                Dot(p12 + 4*vertical_shift*DOWN + i*0.2*DOWN)
                for i in range(3)
            ]
        )
        dots_pow3_anim = [FadeIn(dot, shift=DOWN) for dot in dots_pow3]
        self.play(
            AnimationGroup(*dots_pow2_anim, lag_ratio=0.5),
            AnimationGroup(*dots_pow3_anim, lag_ratio=0.5),
            fp_formula_forx_exp2.animate.shift(DOWN),
            fp_formula_forx_exp3.animate.shift(DOWN), 
        )
        
        self.play(
            AnimationGroup(*[FadeOut(brace, shift=DOWN) for brace in braces], lag_ratio=0.5),
            AnimationGroup(*[FadeOut(brace_text, shift = DOWN) for brace_text in braces_text], lag_ratio=0.5)
        )
        
        self.play(self.camera.frame.animate.shift(1.2*DOWN)) 
        self.wait()

        dots_pow2_anim = [FadeOut(dot, shift=DOWN) for dot in dots_pow2]
        dots_pow3_anim = [FadeOut(dot, shift=DOWN) for dot in dots_pow3]
        
        self.play(
            AnimationGroup(*dots_pow2_anim, lag_ratio=0.5),
            AnimationGroup(*dots_pow3_anim, lag_ratio=0.5),
            Transform(four_boundary, DashedLine(p4, p4 + (boundary_length-5)*DOWN, color = RED) ),
            Transform(eight_boundary, DashedLine(p8, p8 + (boundary_length-5)*DOWN, color = RED) ),
            Transform(sixteen_boundary, DashedLine(p16, p16 + (boundary_length-5)*DOWN, color = RED) ),
            FadeOut(fp_formula_forx_exp3) 
        )

        fp_formula_number_n1 = MathTex().move_to(fp_formula_forx_exp2.get_center())
        def fp_formula_updater_n1(mobj):
            mobj.become(MathTex(f"x = {self.x_fp.get_value():.2f}"))
            mobj.move_to(fp_formula_forx_exp2.get_center())
        fp_formula_updater_n1(fp_formula_number_n1)
        fp_formula_number_n1.add_updater(fp_formula_updater_n1)

        rect_size = (0.5,0.5)
        exponent_blocks_n1 = [
            Rectangle(color=BLACK, fill_opacity = 0.5, fill_color = color_list[0], height=rect_size[1], width=rect_size[0]*8, grid_xstep=rect_size[0])
            .next_to(fp_formula_number_n1, RIGHT, buff = LARGE_BUFF) 
        ]
        exponent_text_n1_inside_blocks = [
            #MathTex(f"{two_bin_string[i]}")
            Integer(number=0, num_decimal_places=0, color = BLACK)
            .move_to(exponent_blocks_n1[0].get_left()+rect_size[0]*i*RIGHT+rect_size[0]/2*RIGHT)
            for i in range(8)
        ]
        for index, e in enumerate(exponent_text_n1_inside_blocks):
            e.index = index
            e.add_updater(write_exponent_bit_value_n1)

        mantissa_blocks_n1 = [
                Rectangle(color=BLACK,fill_opacity=0.5, fill_color=color_list[(i+1)%len(color_list)], height=rect_size[1], width=rect_size[0], grid_xstep=rect_size[0]) 
                .next_to(exponent_blocks_n1[0], RIGHT, buff= LARGE_BUFF+i*rect_size[0])
                for i in range(10)
            ]
        
        mantissa_text_n1_inside_blocks = [
            Integer(number=0, num_decimal_places=0, color = BLACK)
            .move_to(mantissa_blocks_n1[0].get_left()+rect_size[0]*i*RIGHT+rect_size[0]/2*RIGHT)
            for i in range(10)
        ]
        for index, e in enumerate(mantissa_text_n1_inside_blocks):
            e.index = index +1
            e.add_updater(write_mantissa_bit_value_x_fp)

        dots_to_m23_n1 = VGroup(
            *[
                Dot().next_to(mantissa_blocks_n1[-1], RIGHT, buff = MED_SMALL_BUFF*(i+1))
                for i in range(3)
            ]
        )

        m23_rectangle_n1 = Rectangle(color=BLACK,fill_opacity=0.5,
            height=rect_size[1], width=rect_size[0],fill_color = color_list[1],
            grid_xstep=rect_size[0]).next_to(dots_to_m23_n1[-1], RIGHT)
        m23_text_n1_inside_block = Integer(number=0, num_decimal_places=0, color = BLACK
            ).move_to(m23_rectangle_n1.get_center())
        m23_text_n1_inside_block.index = 23
        m23_text_n1_inside_block.add_updater(write_mantissa_bit_value_x_fp)

        exp_blocks_n1_vg = VGroup(*exponent_blocks_n1, *exponent_text_n1_inside_blocks)
        mantissa_blocks_n1_vg = VGroup(*mantissa_blocks_n1, *mantissa_text_n1_inside_blocks)
        m23_n1_vg = VGroup(m23_rectangle_n1, m23_text_n1_inside_block)

        exponent_title = Tex("Exponent").next_to(exp_blocks_n1_vg, UP)
        mantissa_title = Tex("Mantissa").next_to(
            VGroup(
                mantissa_blocks_n1_vg,
                m23_n1_vg
            )
        , UP).align_to(exponent_title, UP)

        x_fp_exp2_label = MathTex(r"{{x}}").next_to(x_fp_exp2, UP)
        x_fp_exp2_label.add_updater(
            lambda mobj: mobj.next_to(x_fp_exp2, UP)
        )
        self.play(
            FadeTransform(fp_formula_forx_exp2, fp_formula_number_n1),
            Write(x_fp_exp2_label)
        )
        self.play(
            #TransformMatchingTex(fp_formula_forx_exp2, fp_formula_number_exp2),
            AnimationGroup(
                Write(exp_blocks_n1_vg),
                Write(mantissa_blocks_n1_vg),
                Write(dots_to_m23_n1),
                Write(m23_n1_vg),
                Write(exponent_title),
                Write(mantissa_title),
                lag_ratio=0.5),
        )
        self.wait() 
        
        self.play(self.x_fp.animate.set_value(15),run_time=2)
        self.play(self.x_fp.animate.set_value(5.39),run_time=2)


        ### N2
        self.y_fp.set_value(7.12)
        y_fp_exp2 = Dot(self.real_line.n2p(self.y_fp.get_value()))
        y_fp_exp2.add_updater(place_dot_y_fp)
        y_fp_exp2_label = MathTex(r"{{y}}").next_to(y_fp_exp2, UP)
        y_fp_exp2_label.add_updater(
            lambda mobj: mobj.next_to(y_fp_exp2, UP)
        )

        fp_formula_number_y = MathTex(f"y = {self.y_fp.get_value():.2f}")
        fp_formula_number_y.next_to(fp_formula_number_n1, DOWN, buff = LARGE_BUFF)
        def fp_formula_updater_n2(mobj):
            mobj.become(MathTex(f"y = {self.y_fp.get_value():.2f}"))
            mobj.next_to(fp_formula_number_n1, DOWN, buff = LARGE_BUFF)
        fp_formula_updater_n2(fp_formula_number_y)
        fp_formula_number_y.add_updater(fp_formula_updater_n2)

        exponent_blocks_n2 = [
            Rectangle(color=BLACK, fill_opacity = 0.5, fill_color = color_list[0], height=rect_size[1], width=rect_size[0]*8, grid_xstep=rect_size[0])
            .next_to(fp_formula_number_y, RIGHT, buff = LARGE_BUFF) 
        ]
        exponent_text_n2_inside_blocks = [
            #MathTex(f"{two_bin_string[i]}")
            Integer(number=0, num_decimal_places=0, color = BLACK)
            .move_to(exponent_blocks_n2[0].get_left()+rect_size[0]*i*RIGHT+rect_size[0]/2*RIGHT)
            for i in range(8)
        ]
        for index, e in enumerate(exponent_text_n2_inside_blocks):
            e.index = index
            e.add_updater(write_exponent_bit_value_n2)

        mantissa_blocks_n2 = [
                Rectangle(color=BLACK,fill_opacity=0.5, fill_color=color_list[(i+1)%len(color_list)], height=rect_size[1], width=rect_size[0], grid_xstep=rect_size[0]) 
                .next_to(exponent_blocks_n2[0], RIGHT, buff= LARGE_BUFF+i*rect_size[0])
                for i in range(10)
            ]
        
        mantissa_text_n2_inside_blocks = [
            Integer(number=0, num_decimal_places=0, color = BLACK)
            .move_to(mantissa_blocks_n2[0].get_left()+rect_size[0]*i*RIGHT+rect_size[0]/2*RIGHT)
            for i in range(10)
        ]
        for index, e in enumerate(mantissa_text_n2_inside_blocks):
            e.index = index +1
            e.add_updater(write_mantissa_bit_value_y_fp)

        dots_to_m23_n2 = VGroup(
            *[
                Dot().next_to(mantissa_blocks_n2[-1], RIGHT, buff = MED_SMALL_BUFF*(i+1))
                for i in range(3)
            ]
        )

        m23_rectangle_n2 = Rectangle(color=BLACK,fill_opacity=0.5,
            height=rect_size[1], width=rect_size[0],fill_color = color_list[1],
            grid_xstep=rect_size[0]).next_to(dots_to_m23_n2[-1], RIGHT)
        m23_text_n2_inside_block = Integer(number=0, num_decimal_places=0, color = BLACK
            ).move_to(m23_rectangle_n2.get_center())
        m23_text_n2_inside_block.index = 23
        m23_text_n2_inside_block.add_updater(write_mantissa_bit_value_x_fp)

        exp_blocks_n2_vg = VGroup(*exponent_blocks_n2, *exponent_text_n2_inside_blocks)
        mantissa_blocks_n2_vg = VGroup(*mantissa_blocks_n2, *mantissa_text_n2_inside_blocks)
        m23_n2_vg = VGroup(m23_rectangle_n2, m23_text_n2_inside_block)

        self.play(
            FadeIn(y_fp_exp2),
            FadeIn(y_fp_exp2_label),
        )
        self.play(
            #TransformMatchingTex(fp_formula_forx_exp2, fp_formula_number_exp2),
            
            AnimationGroup(
                Write(fp_formula_number_y),
                Write(exp_blocks_n2_vg),
                Write(mantissa_blocks_n2_vg),
                Write(dots_to_m23_n2),
                Write(m23_n2_vg),
                lag_ratio=0.5
            ),
        )
        
        original_x_fp = self.x_fp.get_value()-0.01
        # plus_A_line = Arrow(
        #     start=self.real_line.n2p(self.x_fp.get_value()),
        #     end=self.real_line.n2p(self.x_fp.get_value()),
        #     color = BLACK,
        #     stroke_width=15,
        #     #max_tip_length_to_length_ratio= 5.0
        # )
        # plus_A_line.add_tip(tip_length=0.3, tip_width=0.5)
        # plus_A_line.add_updater( 
        #     lambda mobj: mobj.put_start_and_end_on(
        #         self.real_line.n2p(original_x_fp), self.real_line.n2p(self.x_fp.get_value())
        #     )
        # )
        # self.add(
        #     plus_A_line
        # )
        ## COMMON MANTISSA BITS
        self.common_mantissa_bits = 1
        frame_common_mantissa_bits = Rectangle(
            width = np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n1[self.common_mantissa_bits].get_vertices()[0]),
            height = rect_size[0] + np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n2[0].get_vertices()[0]),
            color = RED,
            stroke_width = 8,
        ).move_to(
            (mantissa_blocks_n1[0].get_center() + mantissa_blocks_n2[self.common_mantissa_bits-1].get_center())/2.0
        )
        self.play(
            Write(frame_common_mantissa_bits)
        )
        A = 8.0

        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )
        self.wait(1)
        self.play(
            self.x_fp.animate.increment_value(-A),
            self.y_fp.animate.increment_value(-A),
            run_time=1,
        )

        
        def set_start_end_arrow(mobj):
            mobj.put_start_and_end_on(
                self.real_line.n2p(mobj.start_number) + mobj.vertical_shift,
                self.real_line.n2p(mobj.end_number) + mobj.vertical_shift,
            )

        exp_arrows = []
        for i in positive_power_list[:-1]:
            start_number = 2**i
            end_number = 2**(i+1)
            vertical_shift = DOWN*0.5
            arrow = DoubleArrow(
                start = self.real_line.n2p(start_number) + vertical_shift,
                end = self.real_line.n2p(end_number) + vertical_shift,
                buff = 0,
                color = color_list[0],
            )
            arrow.start_number = start_number
            arrow.end_number = end_number
            arrow.vertical_shift = vertical_shift
            arrow.add_updater(set_start_end_arrow)
            exp_arrows.append(arrow)
        

        m1_arrows = []
        for i in positive_power_list[:-1]:
            for j in range(2):
                start_number = 2**i*(1 + j/2)
                end_number = 2**i*(1 + (j+1)/2)
                vertical_shift = 2*DOWN*0.5
                arrow = DoubleArrow(
                    start = self.real_line.n2p(start_number) + vertical_shift,
                    end = self.real_line.n2p(end_number) + vertical_shift,
                    buff = 0,
                    color = color_list[1],
                )
                arrow.start_number = start_number
                arrow.end_number = end_number
                arrow.vertical_shift = vertical_shift
                arrow.add_updater(set_start_end_arrow)
                m1_arrows.append(arrow)

        m2_arrows = []
        for i in positive_power_list[:-1]:
            for j in range(4):
                start_number = 2**i*(1 + j/4)
                end_number = 2**i*(1 + (j+1)/4)
                vertical_shift = 3*DOWN*0.5
                arrow = DoubleArrow(
                    start = self.real_line.n2p(start_number) + vertical_shift,
                    end = self.real_line.n2p(end_number) + vertical_shift,
                    buff = 0,
                    color = color_list[2],
                )
                arrow.start_number = start_number
                arrow.end_number = end_number
                arrow.vertical_shift = vertical_shift
                arrow.add_updater(set_start_end_arrow)
                m2_arrows.append(arrow)

        m3_arrows = []
        for i in positive_power_list[6:-1]:
            for j in range(8):
                start_number = 2**i*(1 + j/8)
                end_number = 2**i*(1 + (j+1)/8)
                vertical_shift = 4*DOWN*0.5
                arrow = DoubleArrow(
                    start = self.real_line.n2p(start_number) + vertical_shift,
                    end = self.real_line.n2p(end_number) + vertical_shift,
                    buff = 0,
                    color = color_list[3],
                )
                arrow.start_number = start_number
                arrow.end_number = end_number
                arrow.vertical_shift = vertical_shift
                arrow.add_updater(set_start_end_arrow)
                m3_arrows.append(arrow)

        m4_arrows = []
        for i in positive_power_list[7:-1]:
            for j in range(16):
                start_number = 2**i*(1 + j/16)
                end_number = 2**i*(1 + (j+1)/16)
                vertical_shift = 5*DOWN*0.5
                arrow = DoubleArrow(
                    start = self.real_line.n2p(start_number) + vertical_shift,
                    end = self.real_line.n2p(end_number) + vertical_shift,
                    buff = 0,
                    color = color_list[4],
                )
                arrow.start_number = start_number
                arrow.end_number = end_number
                arrow.vertical_shift = vertical_shift
                arrow.add_updater(set_start_end_arrow)
                m4_arrows.append(arrow)

        def set_start_end_boundary(mobj):
            mobj.put_start_and_end_on(
                self.real_line.n2p(mobj.start_number),
                self.real_line.n2p(mobj.start_number) + mobj.len,
            )
        boundaries = []
        for i in positive_power_list:
            boundary = four_boundary.copy()
            boundary.start_number = 2**i
            boundary.len = boundary_length*DOWN/3
            boundary.add_updater(set_start_end_boundary)
            boundaries.append(boundary)
        
        self.play(
            ReplacementTransform(four_boundary, boundaries[3]),
            ReplacementTransform(eight_boundary, boundaries[4]),
            ReplacementTransform(sixteen_boundary, boundaries[5]),

            ReplacementTransform(exp_arr_pow2, exp_arrows[3]),
            FadeOut(exp_arr_pow2_gv.submobjects[1]),
            ReplacementTransform(exp_arr_pow3, exp_arrows[4]),
            FadeOut(exp_arr_pow3_gv.submobjects[1]),

            ReplacementTransform(m1_arr_pow2_gv.submobjects[0], m1_arrows[6]),
            ReplacementTransform(m1_arr_pow2_gv.submobjects[1], m1_arrows[7]),
            FadeOut(*m1_arr_pow2_gv.submobjects[2:]),
            ReplacementTransform(m1_arr_pow3_gv.submobjects[0], m1_arrows[8]),
            ReplacementTransform(m1_arr_pow3_gv.submobjects[1], m1_arrows[9]),
            FadeOut(*m1_arr_pow3_gv.submobjects[2:]),

            ReplacementTransform(m2_arr_pow2_gv.submobjects[0], m2_arrows[12]),
            ReplacementTransform(m2_arr_pow2_gv.submobjects[1], m2_arrows[13]),
            ReplacementTransform(m2_arr_pow2_gv.submobjects[2], m2_arrows[14]),
            ReplacementTransform(m2_arr_pow2_gv.submobjects[3], m2_arrows[15]),
            FadeOut(*m2_arr_pow2_gv.submobjects[4:]),
            ReplacementTransform(m2_arr_pow3_gv.submobjects[0], m2_arrows[16]),
            ReplacementTransform(m2_arr_pow3_gv.submobjects[1], m2_arrows[17]),
            ReplacementTransform(m2_arr_pow3_gv.submobjects[2], m2_arrows[18]),
            ReplacementTransform(m2_arr_pow3_gv.submobjects[3], m2_arrows[19]),
            FadeOut(*m2_arr_pow3_gv.submobjects[4:]),

            FadeIn(*boundaries[6:]),
            FadeIn(*exp_arrows[5:], shift  = UP ),
            FadeIn(*m1_arrows[10:], shift = UP),
            FadeIn(*m2_arrows[20:], shift = UP),
            FadeIn(*m3_arrows, shift = UP),
            FadeIn(*m4_arrows, shift = UP),
        )
        
        A = 8.0
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )
        self.play(
            self.real_line.animate.scale(
                0.5, about_point = self.real_line.n2p(8)
            ).shift(
                LEFT*np.linalg.norm(self.real_line.n2p(8)-self.real_line.n2p(4))
            )
        )

        A = 16.0 - (16/4)
        
        self.common_mantissa_bits = 2
        new_frame_common_mantissa_bits = Rectangle(
            width = np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n1[self.common_mantissa_bits].get_vertices()[0]),
            height = rect_size[0] + np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n2[0].get_vertices()[0]),
            color = RED,
            stroke_width = 8
        ).move_to(
            (mantissa_blocks_n1[0].get_center() + mantissa_blocks_n2[self.common_mantissa_bits-1].get_center())/2.0
        )
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )
        self.play(Transform(frame_common_mantissa_bits,new_frame_common_mantissa_bits))
        self.play(
            self.real_line.animate.scale(
                0.5, about_point = self.real_line.n2p(16)
            ).shift(
                LEFT*np.linalg.norm(self.real_line.n2p(16)-self.real_line.n2p(8))
            ),
            
        )

        A = 32.0 - (32/8)
        
        self.common_mantissa_bits = 3
        new_frame_common_mantissa_bits = Rectangle(
            width = np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n1[self.common_mantissa_bits].get_vertices()[0]),
            height = rect_size[0] + np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n2[0].get_vertices()[0]),
            color = RED,
            stroke_width = 8
        ).move_to(
            (mantissa_blocks_n1[0].get_center() + mantissa_blocks_n2[self.common_mantissa_bits-1].get_center())/2.0
        )
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )
        self.play(Transform(frame_common_mantissa_bits,new_frame_common_mantissa_bits))
        self.play(
            self.real_line.animate.scale(
                0.5, about_point = self.real_line.n2p(32)
            ).shift(
                LEFT*np.linalg.norm(self.real_line.n2p(32)-self.real_line.n2p(16))
            ),
            
        )
        A = 64.0 - (64/16)
        
        self.common_mantissa_bits = 4
        new_frame_common_mantissa_bits = Rectangle(
            width = np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n1[self.common_mantissa_bits].get_vertices()[0]),
            height = rect_size[0] + np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n2[0].get_vertices()[0]),
            color = RED,
            stroke_width = 8
        ).move_to(
            (mantissa_blocks_n1[0].get_center() + mantissa_blocks_n2[self.common_mantissa_bits-1].get_center())/2.0
        )
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )

        self.play(Transform(frame_common_mantissa_bits,new_frame_common_mantissa_bits))
        # self.play(
        #     self.real_line.animate.scale(
        #         0.5, about_point = self.real_line.n2p(32)
        #     ).shift(
        #         LEFT*np.linalg.norm(self.real_line.n2p(32)-self.real_line.n2p(16))
        #     ),
            
        # )
        
        self.camera.frame.save_state()
        ##SHOW WHAT HAPPENS IN TERMS OF ERROR
        self.play(
            self.camera.frame.animate.scale(0.2).move_to(x_fp_exp2),
            FadeOut(y_fp_exp2),
            FadeOut(y_fp_exp2_label),
            #FadeOut(plus_A_line),
        )
        new_real_line = self.real_line.copy()
        new_real_line.x_range[2] = 8.0
        new_real_line.set(
            tick_size = 0.2,
            unit = 8.0
        ).add_ticks()
    

        self.play(
            Write(new_real_line)
            #Transform(self.real_line, new_real_line)
        )
        self.real_line.become(new_real_line)
        self.remove(new_real_line)

        def move_x_point(mobj):
            mobj.move_to(x_fp_exp2.get_center())

        self.camera.frame.add_updater(move_x_point)
        A = 65.4
        self.remove(title_of_the_paper)
        self.add(title_of_the_paper)
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=5,
        )
        
        x_fp_exp2_true = x_fp_exp2.copy().set(color = "#d62828").clear_updaters()
        x_fp_exp2_label_true = MathTex(
            r"{{x}}^*").set(
            color = "#d62828").move_to(
            x_fp_exp2_label, aligned_edge = LEFT + DOWN)
        self.play(FadeIn(x_fp_exp2_true, x_fp_exp2_label_true))

        self.play(
            self.x_fp.animate.set_value(np.floor(self.x_fp.get_value()/8.0)*8.0),
            self.y_fp.animate.set_value(np.floor(self.x_fp.get_value()/8.0)*8.0),
            run_time=1,
        )

        # delta_arrow_forward = DoubleArrow(
        #     buff = 0,
        #     max_tip_length_to_length_ratio=0.2,
        #     start = x_fp_exp2.get_center() + DOWN*0.1,
        #     end = x_fp_exp2_true.get_center()+ DOWN*0.1,
        #     color = "#d62828"
        # )
        delta_arrow_forward = Line(
            start = x_fp_exp2.get_center(),
            end = x_fp_exp2_true.get_center(),
            color = "#d62828"
        )
        delta_arrow_forward_label = MathTex(
            r"\Delta_x",
            font_size = 40,
            color = "#d62828"
        ).next_to(delta_arrow_forward, DOWN*0.1)

        self.play(
            FadeIn(
                delta_arrow_forward,
                delta_arrow_forward_label
            ),
            run_time=1,
        )
        
        self.play(
            self.x_fp.animate.increment_value(-A-0.8),
            self.y_fp.animate.increment_value(-A-0.8),
            run_time=5,
        )
        x_fp_exp2_true_backward = x_fp_exp2.copy().set(color = "#005f73").clear_updaters()
        x_fp_exp2_label_backward_true = MathTex(
            r"{{x}}^*").set(
            color = "#005f73").move_to(x_fp_exp2_label, aligned_edge = LEFT + DOWN)
        self.play(FadeIn(x_fp_exp2_true_backward, x_fp_exp2_label_backward_true))


        self.play(
            self.x_fp.animate.set_value(np.floor(self.x_fp.get_value()/8.0)*8.0 + 8.0),
            self.y_fp.animate.set_value(np.floor(self.x_fp.get_value()/8.0)*8.0 + 8.0),
            run_time=1,
        )

        delta_arrow_backward = Line(
            start = x_fp_exp2.get_center(),
            end = x_fp_exp2_true_backward.get_center(),
            color = "#005f73"
        )
        delta_arrow_backward_label = MathTex(
            r"\Delta_x",
            font_size = 40,
            color = "#005f73"
        ).next_to(delta_arrow_backward, DOWN*0.1)



        self.play(
            FadeIn(
                delta_arrow_backward,
                delta_arrow_backward_label
            ),
            run_time=1,
        )
        self.camera.frame.remove_updater(move_x_point)
        self.play(
            self.camera.frame.animate.scale(3.5).move_to(
                self.real_line.n2p(145)+3.0*UP
            ),
        )
        #self.play(Restore(self.camera.frame))
        
        ### ORIGINAL DATASET

        addition_all_objects = VGroup()

        center_of_image = self.camera.frame_center
        original_x_ds_vg = VGroup(*[
            MathTex(
                r"{{x}}_{{{}}}".format(i)
            ).move_to(center_of_image + 0.5 *UP)
            for i in range(5)
        ])
        original_x_ds_vg.arrange_in_grid(rows = 5, cols = 1, buff = 0.8)
        framebox_original = Rectangle(
            color = BLACK,
            height = original_x_ds_vg.height + 0.5, 
            width = original_x_ds_vg.width + 0.5,
        ).move_to(original_x_ds_vg.get_center())

        addition_all_objects += original_x_ds_vg
        addition_all_objects += framebox_original

        addition_all_objects.move_to(
                center_of_image+ 0.5*UP
        )
        self.play(
            Write(original_x_ds_vg),
            Create(framebox_original),
        )

        ## MOD DATASET
        self.play(addition_all_objects.animate.shift(
            2*LEFT
            )
        )
        arrow_plus_A = Arrow(
            stroke_width = 10,
            color = BLACK
        ).next_to(
            framebox_original,
            RIGHT,
            buff = .2
        )
        arrow_plus_A_label = MathTex("+A").next_to(
            arrow_plus_A, UP, buff = 0.2
        )
        mod_x_ds = []
        for i in range(5):
            x = MathTex(
                r"x_{} + A + \Delta_{{x_{}}}".format(str(i), str(i))
            )
            x.next_to(arrow_plus_A, RIGHT, buff = .4)
            x[0][5:].set(color = "#d62828")
            mod_x_ds.append(x)
        mod_x_ds_vg = VGroup(*mod_x_ds)
        mod_x_ds_vg.arrange_in_grid(rows = 5, cols = 1, buff = 0.05)
        framebox_mod = Rectangle(
            color = "#d62828",
            height = mod_x_ds_vg.height + 0.5, 
            width = mod_x_ds_vg.width + 0.5,
        ).move_to(mod_x_ds_vg.get_center())

        addition_all_objects.add(
            arrow_plus_A,
            arrow_plus_A_label,
            mod_x_ds_vg,
            framebox_mod
        )
        self.play(
            AnimationGroup(   
                GrowArrow(arrow_plus_A),
                Write(arrow_plus_A_label),
                Write(mod_x_ds_vg),
                Create(framebox_mod),
                lag_ratio=0.2,
            )
        )
        
        ## RECOVERED DATASET
        self.play(addition_all_objects.animate.shift(
            3.5*LEFT 
            )
        )
        arrow_minus_A = Arrow(
            stroke_width = 10,
            color = BLACK
        ).next_to(
            framebox_mod,
            RIGHT,
            buff = .2
        )
        arrow_minus_A_label = MathTex("-A").next_to(
            arrow_minus_A, UP, buff = 0.2
        )
        rec_x_ds = []
        for i in range(5):
            x = MathTex(
                r"x_{} + \Delta_{{x_{}}} + \Delta_{{x_{}}} ".format(str(i), str(i), str(i))
            )
            x.next_to(arrow_minus_A,  RIGHT, buff = .4)
            x[0][3:6].set(color = "#d62828")
            x[0][7:].set(color = "#005f73")
            rec_x_ds.append(x)
        rec_x_ds_vg = VGroup(*rec_x_ds)
        rec_x_ds_vg.arrange_in_grid(rows = 5, cols = 1, buff = 0.5)
        framebox_rec = Rectangle(
            color = "#005f73",
            height = framebox_original.height, 
            width = rec_x_ds_vg.width + 0.5,
        ).move_to(rec_x_ds_vg.get_center())
        
        self.play(
            AnimationGroup(   
                GrowArrow(arrow_minus_A),
                Write(arrow_minus_A_label),
                Write(rec_x_ds_vg),
                Create(framebox_rec),
                lag_ratio=0.2,
            )
        )
        addition_all_objects.add(
            arrow_minus_A,
            arrow_minus_A_label,
            rec_x_ds_vg,
            framebox_rec
        )
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title_of_the_paper]
            # All mobjects in the screen are saved in self.mobjects
        )
        self.play(
            Restore(self.camera.frame),
            self.camera.frame.animate.scale(0.9).move_to(0*UP),
        )
        self.wait()
###########
# MULTIPLICATION
###########
        
        start = 1.000
        num_decimal_places = 3 

        x_var_tr = ValueTracker(start)

        x_title = MathTex("x")
        x_times_3_title = MathTex("x \cdot 3")
        x_times_7_title = MathTex("x \cdot 7")
        x_times_13_title = MathTex("x \cdot 13")

        x_var_dec = DecimalNumber(
            start, num_decimal_places=num_decimal_places
        ).add_updater(lambda v: v.set_value(x_var_tr.get_value()), call_updater=True)
        x_var_dec.set(color = BLACK)
        self.x_times_3_var_dec = DecimalNumber(
            start*3, num_decimal_places=num_decimal_places
        ).add_updater(lambda v: v.set_value(x_var_tr.get_value()*3.0), call_updater=True)
        self.x_times_3_var_dec.set(color = BLACK)
        self.x_times_7_var_dec = DecimalNumber(
            start*7, num_decimal_places=num_decimal_places
        ).add_updater(lambda v: v.set_value(x_var_tr.get_value()*7.0), call_updater=True)
        self.x_times_7_var_dec.set(color = BLACK)
        self.x_times_13_var_dec = DecimalNumber(
            start*13, num_decimal_places=num_decimal_places
        ).add_updater(lambda v: v.set_value(x_var_tr.get_value()*13.0), call_updater=True)
        self.x_times_13_var_dec.set(color = BLACK)
        

        # 3

        # def write_result_3(mobj):
        #     control = self.x_times_3_var_dec.get_value()
        #     if int(control) == control:
        #         mobj.set_value(control)
        #         mobj.set(color = BLACK)
            
        result_3_x = MathTex(
            r"1.667",
            color = self.camera.background_color,
        )#.add_updater(write_result_3)
        result_3_y = MathTex(
            r"5.000",
            color = self.camera.background_color,
        )
        # 13
            
        result_13_x = MathTex(
            r"2.077",
            color = self.camera.background_color,
        )
        result_13_y = MathTex(
            r"27.000",
            color = self.camera.background_color,
        )

        # 7
            
        result_7_x = MathTex(
            r"2.714",
            color = self.camera.background_color,
        )
        result_7_y = MathTex(
            r"19.000",
            color = self.camera.background_color,
        )
        multiply_3 = MathTex("M = 3")
        multiply_7 = MathTex("M = 7")
        multiply_13 = MathTex("M = 13")

        variables = VGroup(
            MathTex(""), x_title, x_times_3_title,x_times_7_title,x_times_13_title,
            MathTex(""), x_var_dec, self.x_times_3_var_dec,self.x_times_7_var_dec, self.x_times_13_var_dec,
            multiply_3,result_3_x,result_3_y,MathTex(""),MathTex(""),
            multiply_7,result_7_x,MathTex(""),result_7_y,MathTex(""),
            multiply_13,result_13_x,MathTex(""),MathTex(""),result_13_y,
            #Tex("Mantissa"), x_var_mantissa,x_times_3_mantissa,

        )
        variables.arrange_in_grid(
            rows = 5, cols = 5, col_alignments="rcccc", flow_order="rd",
            buff = (0.6, 0.4)
        )
        variables.move_to(self.camera.frame_center)
        self.play(
            Write(variables)
        )
        #self.add(*variables)
        
        #X
        rectangle_x = SurroundingRectangle(x_var_dec, color = BLACK)
        self.play(
            Create(rectangle_x),
        )
        
        #3
        self.play(x_var_tr.animate.set_value(5/3.0), run_time=2, rate_func=linear)
        rectangle_3_x = SurroundingRectangle(result_3_x, color = GREEN)
        rectangle_3_y = SurroundingRectangle(result_3_y, color = GREEN)
        self.play(
            FadeToColor(result_3_x, BLACK),
            FadeToColor(result_3_y, BLACK),
            Create(rectangle_3_x),
            Create(rectangle_3_y)
        )

        #13
        self.play(x_var_tr.animate.set_value(27.0/13.0), run_time=2, rate_func=linear)
        rectangle_13_x = SurroundingRectangle(result_13_x, color = ORANGE)
        rectangle_13_y = SurroundingRectangle(result_13_y, color = ORANGE)
        self.play(
            FadeToColor(result_13_x, BLACK),
            FadeToColor(result_13_y, BLACK),
            Create(rectangle_13_x),
            Create(rectangle_13_y)
        )

        #7
        self.play(x_var_tr.animate.set_value(19.0/7.0), run_time=2, rate_func=linear)
        rectangle_7_x = SurroundingRectangle(result_7_x, color = BLUE)
        rectangle_7_y = SurroundingRectangle(result_7_y, color = BLUE)
        self.play(
            FadeToColor(result_7_x, BLACK),
            FadeToColor(result_7_y, BLACK),
            Create(rectangle_7_x),
            Create(rectangle_7_y),
        )

        #MANTISSAS
        self.play(
            FadeOut(x_times_3_title,x_times_7_title,x_times_13_title,),
            FadeOut(self.x_times_3_var_dec,self.x_times_7_var_dec, self.x_times_13_var_dec,),

            VGroup(
                x_title, x_var_dec,rectangle_x,
                multiply_3, multiply_7, multiply_13,
                result_3_x, result_7_x, result_13_x,
                rectangle_3_x,rectangle_7_x,rectangle_13_x,

            ).animate.shift(2*LEFT),

            Transform(result_3_y, result_3_y.copy().align_to(result_13_y, RIGHT)),
            Transform(result_7_y, result_7_y.copy().align_to(result_13_y, RIGHT)),
            Transform(result_13_y, result_13_y.copy().align_to(result_13_y, RIGHT)),
            Transform(rectangle_3_y, rectangle_3_y.copy().align_to(rectangle_13_y, RIGHT)),
            Transform(rectangle_7_y, rectangle_7_y.copy().align_to(rectangle_13_y, RIGHT)),
            Transform(rectangle_13_y, rectangle_13_y.copy().align_to(rectangle_13_y, RIGHT)),
        )
        mantissa_title = Tex("x Mantissa").align_to(x_title, UP)
        x_times_3_mantissa = MathTex("1.\overline{10}").align_to(rectangle_3_x, UP)
        x_times_3_mantissa.set(color = BLACK)
        x_times_3_mantissa[0][2].set_color(GREEN)

        x_times_7_mantissa = MathTex("1.01\overline{011}").align_to(rectangle_7_x, UP)
        x_times_7_mantissa.set(color = BLACK)
        x_times_7_mantissa[0][4].set_color(BLUE)

        x_times_13_mantissa = MathTex("1.0\overline{000100111011}").align_to(rectangle_13_x, UP)
        x_times_13_mantissa.set(color = BLACK)
        x_times_13_mantissa[0][3].set_color(ORANGE)

        self.play(
            AnimationGroup(
                Write(mantissa_title),
                Write(x_times_3_mantissa),
                Write(x_times_7_mantissa),
                Write(x_times_13_mantissa),
                lag_ratio=0.2
            )
            
        )
        self.wait()
        
        #Dataset

        ds_title = Tex("Dataset").next_to(x_title, LEFT, buff = 2*MED_LARGE_BUFF)
        x_ds_3 = MathTex("1.652").next_to(rectangle_3_x, LEFT).align_to(ds_title, LEFT)
        x_ds_7 = MathTex("2.651").next_to(rectangle_7_x, LEFT).align_to(ds_title, LEFT)
        x_ds_13 = MathTex("2.071").next_to(rectangle_13_x, LEFT).align_to(ds_title, LEFT)
        self.play(
            Write(ds_title),
            ReplacementTransform(multiply_3, x_ds_3),
            ReplacementTransform(multiply_7, x_ds_7),
            ReplacementTransform(multiply_13, x_ds_13),
        )
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title_of_the_paper]
            # All mobjects in the screen are saved in self.mobjects
        )
        self.wait()
###########
# RESULTS
###########
        ax = Axes(
            x_range = [0, 1, 0.2],
            y_range = [-80, 10, 10],
            axis_config={
                "include_tip": False,
                "font_size": 24,
                "include_numbers": True,
                "color": BLACK,
                "label_direction":UP,
            },
            x_length = 0.3*self.camera.frame.width,
            y_length = 0.6*self.camera.frame.height,
        ).add_coordinates()
        ax.x_axis.numbers.set(color = BLACK)
        ax.y_axis.numbers.set(color = BLACK)
        ax.center()
        y_label = ax.get_y_axis_label(
            Tex("Dataset Size Reduction (\%)").scale(0.65).rotate(90 * DEGREES),
            edge=LEFT, direction=LEFT, buff = 0.4
        )
        x_label = ax.get_x_axis_label(
            Tex("Max Error(\%)").scale(0.65),
            edge=RIGHT, direction=LEFT, buff=-0.4
        ).shift(1.8*RIGHT)
        self.play(
            Write(ax),
            FadeIn(y_label, x_label)
        )
        dashed_lines = VGroup()
        for x in np.arange(0.2, 1.2, 0.2):
            dashed_lines.add(
                ax.get_vertical_line(
                    ax.coords_to_point(x,-80),
                    line_config={
                        "dashed_ratio": 0.55,
                        "stroke_color":GREY,
                    }
                )
            )
        
        for y in np.arange(-80, 10, 10):
            dashed_lines.add(
                ax.get_horizontal_line(
                    ax.coords_to_point(1,y),
                    line_config={
                        "dashed_ratio": 0.55,
                        "stroke_color":GREY,
                    }
                )
            )
        self.play(
            Write(dashed_lines)
        )
        #ax.set(color = BLACK)
        
        dot_config = {
            "radius" : DEFAULT_DOT_RADIUS*2.0,
            "fill_opacity":0.5,
            "stroke_width": 2.0,
            "stroke_color":BLACK,
        }
        star_config = {
            "outer_radius":DEFAULT_DOT_RADIUS*3.0,
            "stroke_color": BLACK,
            "fill_opacity":0.5,
            "stroke_width": 2.0,
        }
        # CBB
        dot_add_cbb = [
            Dot(
                ax.coords_to_point(1, -33),
                fill_color = GREEN,
                **dot_config,
            ),
            Dot(
                ax.coords_to_point(0.2, -21),
                fill_color = GREEN,
                **dot_config,
            ),
            Dot(
                ax.coords_to_point(0.01, -8),
                fill_color = GREEN,
                **dot_config,
            ),
        ]
        star_add_cbb = [
            Star(
                fill_color = GREEN,
                **star_config
            ).move_to(
                ax.coords_to_point(0.13, 0.0)
            )
        ]
        triangle_add_cbb = [
            Triangle(
                fill_color = GREEN, 
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.97, -36)
            ),
            Triangle(
                fill_color = GREEN,
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.12, -8)
            ),
            Triangle(
                fill_color = GREEN,
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.03, 3)
            ),
        ]
        # CBB_dim2
        dot_add_cbb_dim2 = [
            Dot(
                ax.coords_to_point(0.9, -54),
                fill_color = RED,
                **dot_config,
            ),
            Dot(
                ax.coords_to_point(0.342, -48.3),
                fill_color = RED,
                **dot_config,
            ),
            Dot(
                ax.coords_to_point(0.14, -38.8),
                fill_color = RED,
                **dot_config,
            ),
        ]
        triangle_add_cbb_dim2 = [
            Triangle(
                fill_color = RED, 
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(1, -80)
            ),
            Triangle(
                fill_color = RED,
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.61, -65.3)
            ),
            Triangle(
                fill_color = RED,
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.13, -49.3)
            )
        ]
        star_add_cbb_dim2 = [
            Star(
                fill_color = RED,
                **star_config
            ).move_to(
                ax.coords_to_point(0.72, -48.1)
            ),
            Star(
                fill_color = RED,
                **star_config
            ).move_to(
                ax.coords_to_point(0.38, -42.5)
            ),
            Star(
                fill_color = RED,
                **star_config
            ).move_to(
                ax.coords_to_point(0.017, -22.1)
            ),
        ]
        ## LEGEND
        legend_color = Tex(
            "COLORS: Datasets",
            font_size = 30
        )
        legend_triangle = Triangle(
            radius=DEFAULT_DOT_RADIUS*2.0,
            color= GREEN,
            fill_opacity=0.5,
            stroke_width= 2.0,
            stroke_color=BLACK,
            fill_color=self.camera.background_color,
        ).rotate(60*DEGREES).scale(1.2).next_to(legend_color, DOWN).shift(LEFT)
        legend_triangle_desc = Tex(
            ": Multiplication",
            font_size = 30
        ).next_to(legend_triangle, RIGHT)
        legend_dot = Dot(
            radius=DEFAULT_DOT_RADIUS*2.0,
            color= GREEN,
            fill_opacity=0.5,
            stroke_width= 2.0,
            stroke_color=BLACK,
            fill_color=self.camera.background_color,
        ).next_to(legend_color, 2.5*DOWN).shift(LEFT)
        legend_dot_desc = Tex(
            ": Addition",
            font_size = 30
        ).next_to(legend_dot, RIGHT)
        legend_star = Star(
            outer_radius=DEFAULT_DOT_RADIUS*3.0,
            color= GREEN,
            fill_opacity=0.5,
            stroke_width= 2.0,
            stroke_color=BLACK,
            fill_color=self.camera.background_color,
        ).next_to(legend_color, 4*DOWN).shift(LEFT)
        legend_star_desc = Tex(
            ": Info",
            font_size = 30
        ).next_to(legend_star, RIGHT)
        legend_tot = VGroup(
            legend_color,
            legend_triangle,
            legend_triangle_desc,
            legend_dot,
            legend_dot_desc,
            legend_star,
            legend_star_desc,
        ).align_on_border(RIGHT)


        self.play(
            FadeIn(legend_tot),
        )
        
        self.play(
            AnimationGroup(
                FadeIn(*dot_add_cbb,scale=1.5),
                FadeIn(*star_add_cbb,scale=1.5),
                FadeIn(*triangle_add_cbb,scale=1.5),
                lag_ratio=0.2,
            )
        )
        self.play(
            AnimationGroup(
                FadeIn(*dot_add_cbb_dim2,scale=1.5),
                FadeIn(*star_add_cbb_dim2,scale=1.5),
                FadeIn(*triangle_add_cbb_dim2,scale=1.5),
                lag_ratio=0.2,
            )
        )
        self.wait()
###########
# END
###########
class AdditionMethod(MovingCameraScene):#Slide, MovingCameraScene):
    #config["frame_rate"] = 6
    def construct(self):            
        def place_at_the_top_of_frame(mobj):
            mobj.move_to(self.camera.frame_center + UP*(self.camera.frame_height/2)*0.9 )
            mobj.rescale_to_fit(self.camera.frame_width*0.8, 0)
            mobj.underline.set_stroke(width = self.camera.frame_height/10)
        def write_exponent_bit_value_n1(mobj):
            x_fp_exp = su.getFPUnbiasedExponent32bits(self.x_fp.get_value())
            exp_bin = bin(x_fp_exp)[2:].rjust(8, "0")
            #mobj.become(MathTex(f"{x_fp_exp % (2**(mobj.index+1))}"))
            mobj.set_value(int(exp_bin[mobj.index]))
        def write_exponent_bit_value_n2(mobj):
            y_fp_exp = su.getFPUnbiasedExponent32bits(self.y_fp.get_value())
            exp_bin = bin(y_fp_exp)[2:].rjust(8, "0")
            mobj.set_value(int(exp_bin[mobj.index]))
        def write_mantissa_bit_value_x_fp(mobj):
            x_fp_mantissa = su.getLongIntFromSingleMantissa(self.x_fp.get_value())
            mantissa_bin = bin(x_fp_mantissa)[2:].rjust(23, "0")
            mobj.set_value(int(mantissa_bin[mobj.index-1]))
        def write_mantissa_bit_value_y_fp(mobj):
            y_fp_mantissa = su.getLongIntFromSingleMantissa(self.y_fp.get_value())
            mantissa_bin = bin(y_fp_mantissa)[2:].rjust(23, "0")
            mobj.set_value(int(mantissa_bin[mobj.index-1]))
        def place_dot_x_fp(mobj):
            mobj.move_to(self.real_line.n2p(self.x_fp.get_value()))
        def place_dot_y_fp(mobj):
            mobj.move_to(self.real_line.n2p(self.y_fp.get_value()))

        self.camera.frame.save_state() 
        self.camera.background_color = "#edf2f4"
        color_list = [ RED, "#E3B505", "#654F6F", "#107E7D", "#FF784F",]
        Text.set_default(color=BLACK)
        BraceBetweenPoints.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        DashedLine.set_default(color=BLACK)
        Dot.set_default(color=BLACK)
        DoubleArrow.set_default(max_tip_length_to_length_ratio=0.5)
        x_power_min = 8
        x_power_max = 8
        negative_powers_list = list(range(x_power_min+1, 0, -1))
        positive_power_list = list(range(-1, x_power_max+1))
        lab1 = [MathTex(r"-2^{{{}}}".format(power)) for power in negative_powers_list]
        lab2 = [MathTex(r"0")]
        lab3 = [MathTex(r"2^{{{}}}".format(power)) for power in positive_power_list]
        x_labels = [*lab1, *lab2, *lab3]
        title_of_the_paper = Title(f"Change a bit to save a byte, Francesco Taurone et al.",
            stroke_color = BLACK, font_size = 40, underline_buff=SMALL_BUFF).add_updater(place_at_the_top_of_frame)
        title_of_the_paper.underline.set_color(BLACK)
        self.add(title_of_the_paper) 
        ##SECTION

        self.real_line = NumberLine(
            x_range=[-2**x_power_min, 2**x_power_max, 0.5],
            length=52*config.frame_width,
            color=WHITE,
            include_numbers=False,
            label_direction=UP,
            include_tip=True,
            stroke_color = BLACK
            #numbers_to_include = x_values,
            #decimal_number_config = {"num_decimal_places": 0},
        )
        self.play(Write(self.real_line))
        for i in range(len(lab1)):
            lab1[i].power = negative_powers_list[i]
            lab1[i].add_updater(
                update_function = 
                    lambda mobj: mobj.move_to(
                    self.real_line.n2p(-2.0**mobj.power) + UP*0.5
                    ),
                call_updater = True
            )
        for i in range(len(lab2)):
            lab2[i].power = 0
            lab2[i].add_updater(
                update_function = 
                    lambda mobj: mobj.move_to(
                    self.real_line.n2p(0) + UP*0.5
                    ),
                call_updater = True
            )
        for i in range(len(lab3)):
            lab3[i].power = positive_power_list[i]
            lab3[i].add_updater(
                update_function = 
                    lambda mobj: mobj.move_to(
                    self.real_line.n2p(2.0**mobj.power) + UP*0.5
                    ),
                call_updater = True
            )
        
        self.play(AnimationGroup(*[Write(label) for label in x_labels]))
        brace1 = BraceBetweenPoints(self.real_line.n2p(0.5),self.real_line.n2p(1.0), direction=UP, buff = 1.0)
        brace1_text = Tex("$2^{23}$ numbers").next_to(brace1, UP)
        brace2 = BraceBetweenPoints(self.real_line.n2p(1),self.real_line.n2p(2), direction=DOWN, buff = 0.2)
        brace2_text = Tex("$2^{23}$ numbers").next_to(brace2, DOWN)
        brace3 = BraceBetweenPoints(self.real_line.n2p(2),self.real_line.n2p(4), direction=UP, buff =1.0)
        brace3_text = Tex("$2^{23}$ numbers").next_to(brace3, UP)
        brace4 = BraceBetweenPoints(self.real_line.n2p(4),self.real_line.n2p(8), direction=UP, buff =1.0)
        brace4_text = Tex("$2^{23}$ numbers").next_to(brace4, UP)
        brace5 = BraceBetweenPoints(self.real_line.n2p(8),self.real_line.n2p(16), direction=UP, buff =1.0)
        brace5_text = Tex("$2^{23}$ numbers").next_to(brace5, UP)
        braces = [brace1, brace2, brace3, brace4, brace5]
        braces_text = [brace1_text, brace2_text, brace3_text, brace4_text, brace5_text]
        real_line_vg = VGroup(self.real_line,
                              brace1, brace1_text,
                              brace2, brace2_text,
                              brace3, brace3_text,
                              brace4, brace4_text,
                              brace5, brace5_text,
        )
        self.wait()
        self.play(FadeIn(brace1), FadeIn(brace1_text),
                  FadeIn(brace2), FadeIn(brace2_text),
                  FadeIn(brace3), FadeIn(brace3_text),
                  FadeIn(brace4), FadeIn(brace4_text),
                  FadeIn(brace5), FadeIn(brace5_text),
        )
        self.wait()
        self.play(self.camera.frame.animate.move_to(self.real_line.n2p(10)))
        self.play(self.camera.frame.animate.scale(1.5),
            #title_of_the_paper.animate.scale(1.5)          
        )
        #self.play(self.camera.frame.animate.shift())
        self.play(real_line_vg.animate.shift(2.75*UP))
        self.wait()
        
        ## X DEFINITION
        self.x_fp = ValueTracker(5.39)
        self.y_fp = ValueTracker(15.12)
        x_fp_exp2 = Dot(self.real_line.n2p(self.x_fp.get_value()))
        x_fp_exp2.add_updater(place_dot_x_fp)
        x_fp_exp3 = Dot(self.real_line.n2p(self.y_fp.get_value()))
        x_fp_exp3.add_updater(place_dot_y_fp)
        x_fp_exp2_label = MathTex(r"{{x}}").next_to(x_fp_exp2, DOWN)
        x_fp_exp3_label = MathTex(r"{{x}}_2").next_to(x_fp_exp3, DOWN)
        self.play(Indicate(x_fp_exp2), Indicate(x_fp_exp2_label), 
                  #Indicate(x_fp_exp3), Indicate(x_fp_exp3_label)
        )
        self.wait(1)
        fp_formula = MathTex(r"{{x}} = (-1)^S \cdot 2^{E-127}\cdot\left(2^{23} + \sum_{i = 1}^{23}m_i \cdot 2^{23-i}\right)").move_to(self.camera.frame_center)
        fp_formula_onedot = MathTex(r"{{x}} = (-1)^S \cdot 2^{E-127}\cdot\left(1.m_1m_2\dotsm m_{23}\right)"
                            ).move_to(self.camera.frame_center)
        fp_formula_forx_exp2 = MathTex(r"{{x}}{{ = 2^{ {2} }\cdot\left(1.}}{{m_1}}{{m_2}}{{\dotsm m_{23}\right)}}",
                            ).next_to(self.real_line.n2p(6), DOWN, buff = 1.0)
        fp_formula_forx_exp3 = MathTex(r"{{x}}{{ = 2^{ {3} }\cdot\left(1.}}{{m_1}}{{m_2}}{{\dotsm m_{23}\right)}}",
                             ).next_to(self.real_line.n2p(12), DOWN, buff=1.0)
        #self.play(Write(fp_formula))
        
        #self.add(index_labels(fp_formula_forx_exp2[0]))
        fp_formula_forx_exp2[1][2].set_color(color_list[0])
        fp_formula_forx_exp2.set_color_by_tex("m_1", color_list[1])
        fp_formula_forx_exp2.set_color_by_tex("m_2", color_list[2])
        fp_formula_forx_exp3[1][2].set_color(color_list[0])
        fp_formula_forx_exp3.set_color_by_tex("m_1", color_list[1])
        fp_formula_forx_exp3.set_color_by_tex("m_2", color_list[2])
        self.play(TransformMatchingTex(x_fp_exp2_label, fp_formula),
                   #TransformMatchingTex(x_fp_exp3_label, fp_formula)
        )
        self.wait(1)
        self.play(TransformMatchingTex(fp_formula, fp_formula_onedot))
        self.wait(1)
        self.play(TransformMatchingTex(fp_formula_onedot.copy(), fp_formula_forx_exp2),
                   TransformMatchingTex(fp_formula_onedot, fp_formula_forx_exp3) )
        self.wait(1)
        ## mantissa boundary
        boundary_length = 8 
        p4 = self.real_line.n2p(4)
        p8 = self.real_line.n2p(8)
        p16 = self.real_line.n2p(16)
        four_boundary= DashedLine(p4, p4 + boundary_length*DOWN, color = RED) 
        eight_boundary= DashedLine(p8, p8 + boundary_length*DOWN, color = RED) 
        sixteen_boundary= DashedLine(p16, p16 + boundary_length*DOWN, color = RED) 

        self.play(Write(four_boundary),
                  Write(eight_boundary),
                  Write(sixteen_boundary),
        )
        self.wait(1)
        
        vertical_shift = 1

        ## Exponent Arrow
        exp_arr_pow2 = DoubleArrow(p4+ vertical_shift*DOWN, p8+vertical_shift*DOWN, buff=0, color=color_list[0])
        exp_arr_pow2_gv =  VGroup(exp_arr_pow2, MathTex(r"E_U = 2", color = color_list[0]).next_to(exp_arr_pow2, UP, buff = 0.1))
        exp_arr_pow3 = DoubleArrow(p8 +vertical_shift*DOWN, p16+vertical_shift*DOWN, buff=0, color=color_list[0])
        exp_arr_pow3_gv = VGroup(exp_arr_pow3, MathTex(r"E_U = 3", color = color_list[0]).next_to(exp_arr_pow3, UP, buff = 0.1))

        self.play(
            fp_formula_forx_exp2.animate.shift(DOWN),
            fp_formula_forx_exp3.animate.shift(DOWN),
            FadeIn(exp_arr_pow2_gv),
            FadeIn(exp_arr_pow3_gv),
        )
        # self.wait(1)

        ## m1 Arrow
        p6 = self.real_line.n2p(6)
        p12 = self.real_line.n2p(12)
        m1_arr_pow2_1 = DoubleArrow(p4+ 2*vertical_shift*DOWN, p6+2*vertical_shift*DOWN, buff=0, color=color_list[1])
        m1_arr_pow2_2 = DoubleArrow(p6+ 2*vertical_shift*DOWN, p8+2*vertical_shift*DOWN, buff=0, color=color_list[1])
        m1_arr_pow2_gv =  VGroup(
            m1_arr_pow2_1,
            m1_arr_pow2_2,
            MathTex(r"m_1 = 0", color = color_list[1]).next_to(m1_arr_pow2_1, UP, buff = 0.1),
            MathTex(r"m_1 = 1", color = color_list[1]).next_to(m1_arr_pow2_2, UP, buff = 0.1),
        )
        m1_arr_pow3_1 = DoubleArrow(p8 +2*vertical_shift*DOWN, p12+2*vertical_shift*DOWN, buff=0, color=color_list[1])
        m1_arr_pow3_2 = DoubleArrow(p12 +2*vertical_shift*DOWN, p16+2*vertical_shift*DOWN, buff=0, color=color_list[1])
        m1_arr_pow3_gv = VGroup(
            m1_arr_pow3_1,
            m1_arr_pow3_2,
            MathTex(r"m_1 = 0", color = color_list[1]).next_to(m1_arr_pow3_1, UP, buff = 0.1),
            MathTex(r"m_1 = 1", color = color_list[1]).next_to(m1_arr_pow3_2, UP, buff = 0.1),
        )

        self.play(
            fp_formula_forx_exp2.animate.shift(DOWN),
            fp_formula_forx_exp3.animate.shift(DOWN),
            FadeIn(m1_arr_pow2_gv),
            FadeIn(m1_arr_pow3_gv ),
        )
        # self.wait(1)

        ## m2 Arrow
        p5 = self.real_line.n2p(5)
        p7 = self.real_line.n2p(7)
        p10 = self.real_line.n2p(10)
        p14 = self.real_line.n2p(14)
        m2_arr_pow2_1 = DoubleArrow(p4+ 3*vertical_shift*DOWN, p5+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow2_2 = DoubleArrow(p5+ 3*vertical_shift*DOWN, p6+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow2_3 = DoubleArrow(p6+ 3*vertical_shift*DOWN, p7+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow2_4 = DoubleArrow(p7+ 3*vertical_shift*DOWN, p8+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        
        m2_arr_pow2_gv =  VGroup(
            m2_arr_pow2_1,
            m2_arr_pow2_2,
            m2_arr_pow2_3,
            m2_arr_pow2_4,
            MathTex(r"m_2 = 0", color = color_list[2], font_size=40).next_to(m2_arr_pow2_1, UP, buff = 0.1),
            MathTex(r"m_2 = 1", color = color_list[2], font_size=40).next_to(m2_arr_pow2_2, UP, buff = 0.1),
            MathTex(r"m_2 = 0", color = color_list[2], font_size=40).next_to(m2_arr_pow2_3, UP, buff = 0.1),
            MathTex(r"m_2 = 1", color = color_list[2], font_size=40).next_to(m2_arr_pow2_4, UP, buff = 0.1),
        )

        m2_arr_pow3_1 = DoubleArrow(p8 +3*vertical_shift*DOWN, p10+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow3_2 = DoubleArrow(p10 +3*vertical_shift*DOWN, p12+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow3_3 = DoubleArrow(p12 +3*vertical_shift*DOWN, p14+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        m2_arr_pow3_4 = DoubleArrow(p14 +3*vertical_shift*DOWN, p16+3*vertical_shift*DOWN, buff=0, color=color_list[2])
        
        m2_arr_pow3_gv = VGroup(
            m2_arr_pow3_1,
            m2_arr_pow3_2,
            m2_arr_pow3_3,
            m2_arr_pow3_4,
            MathTex(r"m_2 = 0", color = color_list[2], font_size=40).next_to(m2_arr_pow3_1, UP, buff = 0.1),
            MathTex(r"m_2 = 1", color = color_list[2], font_size=40).next_to(m2_arr_pow3_2, UP, buff = 0.1),
            MathTex(r"m_2 = 0", color = color_list[2], font_size=40).next_to(m2_arr_pow3_3, UP, buff = 0.1),
            MathTex(r"m_2 = 1", color = color_list[2], font_size=40).next_to(m2_arr_pow3_4, UP, buff = 0.1),
        )

        self.play(
            fp_formula_forx_exp2.animate.shift(DOWN),
            fp_formula_forx_exp3.animate.shift(DOWN),
            FadeIn(m2_arr_pow2_gv),
            FadeIn(m2_arr_pow3_gv ),
        )
        # self.wait(1)
        #dots
        dots_pow2 = VGroup(
            *[
                Dot(p6 + 4*vertical_shift*DOWN + i*0.2*DOWN)
                for i in range(3)
            ]
        )
        dots_pow2_anim = [FadeIn(dot, shift=DOWN) for dot in dots_pow2]

        dots_pow3 = VGroup(
            *[
                Dot(p12 + 4*vertical_shift*DOWN + i*0.2*DOWN)
                for i in range(3)
            ]
        )
        dots_pow3_anim = [FadeIn(dot, shift=DOWN) for dot in dots_pow3]
        self.play(
            AnimationGroup(*dots_pow2_anim, lag_ratio=0.5),
            AnimationGroup(*dots_pow3_anim, lag_ratio=0.5),
            fp_formula_forx_exp2.animate.shift(DOWN),
            fp_formula_forx_exp3.animate.shift(DOWN), 
        )
        
        self.play(
            AnimationGroup(*[FadeOut(brace, shift=DOWN) for brace in braces], lag_ratio=0.5),
            AnimationGroup(*[FadeOut(brace_text, shift = DOWN) for brace_text in braces_text], lag_ratio=0.5)
        )
        self.play(self.camera.frame.animate.shift(1.5*DOWN)) 

        dots_pow2_anim = [FadeOut(dot, shift=DOWN) for dot in dots_pow2]
        dots_pow3_anim = [FadeOut(dot, shift=DOWN) for dot in dots_pow3]
        
        self.play(
            AnimationGroup(*dots_pow2_anim, lag_ratio=0.5),
            AnimationGroup(*dots_pow3_anim, lag_ratio=0.5),
            Transform(four_boundary, DashedLine(p4, p4 + (boundary_length-5)*DOWN, color = RED) ),
            Transform(eight_boundary, DashedLine(p8, p8 + (boundary_length-5)*DOWN, color = RED) ),
            Transform(sixteen_boundary, DashedLine(p16, p16 + (boundary_length-5)*DOWN, color = RED) ),
        )


        self.play(
            #fp_formula_forx_exp2.animate.move_to(self.camera.frame_center),
            FadeOut(fp_formula_forx_exp3) 
        )
        #fp_formula_number_exp2 = MathTex(r"{{5.39}}{{ = 2^{ {2} }\cdot\left(1.}}{{0}}{{1}}{{\dotsm 1\right)}}",
        #                    ).move_to(fp_formula_forx_exp2.get_center())
        #fp_formula_number_exp2[1][2].set_color(color_list[0])
        #fp_formula_number_exp2[2].set_color(color_list[1])
        #fp_formula_number_exp2[3].set_color(color_list[2])
        fp_formula_number_n1 = MathTex().move_to(fp_formula_forx_exp2.get_center())
        def fp_formula_updater_n1(mobj):
            mobj.become(MathTex(f"x = {self.x_fp.get_value():.2f}"))
            mobj.move_to(fp_formula_forx_exp2.get_center())
        fp_formula_updater_n1(fp_formula_number_n1)
        fp_formula_number_n1.add_updater(fp_formula_updater_n1)

        rect_size = (0.5,0.5)
        exponent_blocks_n1 = [
            Rectangle(color=BLACK, fill_opacity = 0.5, fill_color = color_list[0], height=rect_size[1], width=rect_size[0]*8, grid_xstep=rect_size[0])
            .next_to(fp_formula_number_n1, RIGHT, buff = LARGE_BUFF) 
        ]
        exponent_text_n1_inside_blocks = [
            #MathTex(f"{two_bin_string[i]}")
            Integer(number=0, num_decimal_places=0, color = BLACK)
            .move_to(exponent_blocks_n1[0].get_left()+rect_size[0]*i*RIGHT+rect_size[0]/2*RIGHT)
            for i in range(8)
        ]
        for index, e in enumerate(exponent_text_n1_inside_blocks):
            e.index = index
            e.add_updater(write_exponent_bit_value_n1)

        mantissa_blocks_n1 = [
                Rectangle(color=BLACK,fill_opacity=0.5, fill_color=color_list[(i+1)%len(color_list)], height=rect_size[1], width=rect_size[0], grid_xstep=rect_size[0]) 
                .next_to(exponent_blocks_n1[0], RIGHT, buff= LARGE_BUFF+i*rect_size[0])
                for i in range(10)
            ]
        
        mantissa_text_n1_inside_blocks = [
            Integer(number=0, num_decimal_places=0, color = BLACK)
            .move_to(mantissa_blocks_n1[0].get_left()+rect_size[0]*i*RIGHT+rect_size[0]/2*RIGHT)
            for i in range(10)
        ]
        for index, e in enumerate(mantissa_text_n1_inside_blocks):
            e.index = index +1
            e.add_updater(write_mantissa_bit_value_x_fp)

        dots_to_m23_n1 = VGroup(
            *[
                Dot().next_to(mantissa_blocks_n1[-1], RIGHT, buff = MED_SMALL_BUFF*(i+1))
                for i in range(3)
            ]
        )

        m23_rectangle_n1 = Rectangle(color=BLACK,
            height=rect_size[1], width=rect_size[0],
            grid_xstep=rect_size[0]).next_to(dots_to_m23_n1[-1], RIGHT)
        m23_text_n1_inside_block = Integer(number=0, num_decimal_places=0, color = BLACK
            ).move_to(m23_rectangle_n1.get_center())
        m23_text_n1_inside_block.index = 23
        m23_text_n1_inside_block.add_updater(write_mantissa_bit_value_x_fp)

        exp_blocks_n1_vg = VGroup(*exponent_blocks_n1, *exponent_text_n1_inside_blocks)
        mantissa_blocks_n1_vg = VGroup(*mantissa_blocks_n1, *mantissa_text_n1_inside_blocks)
        m23_n1_vg = VGroup(m23_rectangle_n1, m23_text_n1_inside_block)

        exponent_title = Tex("Exponent").next_to(exp_blocks_n1_vg, UP)
        mantissa_title = Tex("Mantissa").next_to(
            VGroup(
                mantissa_blocks_n1_vg,
                m23_n1_vg
            )
        , UP).align_to(exponent_title, UP)

        x_fp_exp2_label = MathTex(r"{{x}}").next_to(x_fp_exp2, UP)
        x_fp_exp2_label.add_updater(
            lambda mobj: mobj.next_to(x_fp_exp2, UP)
        )
        self.play(
            FadeTransform(fp_formula_forx_exp2, fp_formula_number_n1),
            Write(x_fp_exp2_label)
        )
        self.play(
            #TransformMatchingTex(fp_formula_forx_exp2, fp_formula_number_exp2),
            AnimationGroup(
                Write(exp_blocks_n1_vg),
                Write(mantissa_blocks_n1_vg),
                Write(dots_to_m23_n1),
                Write(m23_n1_vg),
                Write(exponent_title),
                Write(mantissa_title),
                lag_ratio=0.5),
        )
        
        self.play(self.x_fp.animate.set_value(15),run_time=1)
        self.play(self.x_fp.animate.set_value(5.39),run_time=1)


        ### N2
        self.y_fp.set_value(7.12)
        y_fp_exp2 = Dot(self.real_line.n2p(self.y_fp.get_value()))
        y_fp_exp2.add_updater(place_dot_y_fp)
        y_fp_exp2_label = MathTex(r"{{y}}").next_to(y_fp_exp2, UP)
        y_fp_exp2_label.add_updater(
            lambda mobj: mobj.next_to(y_fp_exp2, UP)
        )

        fp_formula_number_y = MathTex(f"y = {self.y_fp.get_value():.2f}")
        fp_formula_number_y.next_to(fp_formula_number_n1, DOWN, buff = LARGE_BUFF)
        def fp_formula_updater_n2(mobj):
            mobj.become(MathTex(f"y = {self.y_fp.get_value():.2f}"))
            mobj.next_to(fp_formula_number_n1, DOWN, buff = LARGE_BUFF)
        fp_formula_updater_n2(fp_formula_number_y)
        fp_formula_number_y.add_updater(fp_formula_updater_n2)

        exponent_blocks_n2 = [
            Rectangle(color=BLACK, fill_opacity = 0.5, fill_color = color_list[0], height=rect_size[1], width=rect_size[0]*8, grid_xstep=rect_size[0])
            .next_to(fp_formula_number_y, RIGHT, buff = LARGE_BUFF) 
        ]
        exponent_text_n2_inside_blocks = [
            #MathTex(f"{two_bin_string[i]}")
            Integer(number=0, num_decimal_places=0, color = BLACK)
            .move_to(exponent_blocks_n2[0].get_left()+rect_size[0]*i*RIGHT+rect_size[0]/2*RIGHT)
            for i in range(8)
        ]
        for index, e in enumerate(exponent_text_n2_inside_blocks):
            e.index = index
            e.add_updater(write_exponent_bit_value_n2)

        mantissa_blocks_n2 = [
                Rectangle(color=BLACK,fill_opacity=0.5, fill_color=color_list[(i+1)%len(color_list)], height=rect_size[1], width=rect_size[0], grid_xstep=rect_size[0]) 
                .next_to(exponent_blocks_n2[0], RIGHT, buff= LARGE_BUFF+i*rect_size[0])
                for i in range(10)
            ]
        
        mantissa_text_n2_inside_blocks = [
            Integer(number=0, num_decimal_places=0, color = BLACK)
            .move_to(mantissa_blocks_n2[0].get_left()+rect_size[0]*i*RIGHT+rect_size[0]/2*RIGHT)
            for i in range(10)
        ]
        for index, e in enumerate(mantissa_text_n2_inside_blocks):
            e.index = index +1
            e.add_updater(write_mantissa_bit_value_y_fp)

        dots_to_m23_n2 = VGroup(
            *[
                Dot().next_to(mantissa_blocks_n2[-1], RIGHT, buff = MED_SMALL_BUFF*(i+1))
                for i in range(3)
            ]
        )

        m23_rectangle_n2 = Rectangle(color=BLACK,
            height=rect_size[1], width=rect_size[0],
            grid_xstep=rect_size[0]).next_to(dots_to_m23_n2[-1], RIGHT)
        m23_text_n2_inside_block = Integer(number=0, num_decimal_places=0, color = BLACK
            ).move_to(m23_rectangle_n2.get_center())
        m23_text_n2_inside_block.index = 23
        m23_text_n2_inside_block.add_updater(write_mantissa_bit_value_x_fp)

        exp_blocks_n2_vg = VGroup(*exponent_blocks_n2, *exponent_text_n2_inside_blocks)
        mantissa_blocks_n2_vg = VGroup(*mantissa_blocks_n2, *mantissa_text_n2_inside_blocks)
        m23_n2_vg = VGroup(m23_rectangle_n2, m23_text_n2_inside_block)

        self.play(
            FadeIn(y_fp_exp2),
            FadeIn(y_fp_exp2_label),
        )
        self.play(
            #TransformMatchingTex(fp_formula_forx_exp2, fp_formula_number_exp2),
            
            AnimationGroup(
                Write(fp_formula_number_y),
                Write(exp_blocks_n2_vg),
                Write(mantissa_blocks_n2_vg),
                Write(dots_to_m23_n2),
                Write(m23_n2_vg),
                lag_ratio=0.5
            ),
        )
        
        original_x_fp = self.x_fp.get_value()-0.01
        plus_A_line = Arrow(
            start=self.real_line.n2p(self.x_fp.get_value()),
            end=self.real_line.n2p(self.x_fp.get_value()),
            color = BLACK,
            stroke_width=15,
            #max_tip_length_to_length_ratio= 5.0
        )
        plus_A_line.add_tip(tip_length=0.3, tip_width=0.5)
        plus_A_line.add_updater( 
            lambda mobj: mobj.put_start_and_end_on(
                self.real_line.n2p(original_x_fp), self.real_line.n2p(self.x_fp.get_value())
            )
        )
        self.add(plus_A_line)
        ## COMMON MANTISSA BITS
        self.common_mantissa_bits = 1
        frame_common_mantissa_bits = Rectangle(
            width = np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n1[self.common_mantissa_bits].get_vertices()[0]),
            height = rect_size[0] + np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n2[0].get_vertices()[0]),
            color = RED,
            stroke_width = 8,
        ).move_to(
            (mantissa_blocks_n1[0].get_center() + mantissa_blocks_n2[self.common_mantissa_bits-1].get_center())/2.0
        )
        self.add(frame_common_mantissa_bits)
        A = 8.0

        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )
        self.play(
            self.x_fp.animate.increment_value(-A),
            self.y_fp.animate.increment_value(-A),
            run_time=1,
        )

        
        def set_start_end_arrow(mobj):
            mobj.put_start_and_end_on(
                self.real_line.n2p(mobj.start_number) + mobj.vertical_shift,
                self.real_line.n2p(mobj.end_number) + mobj.vertical_shift,
            )

        exp_arrows = []
        for i in positive_power_list[:-1]:
            start_number = 2**i
            end_number = 2**(i+1)
            vertical_shift = DOWN*0.5
            arrow = DoubleArrow(
                start = self.real_line.n2p(start_number) + vertical_shift,
                end = self.real_line.n2p(end_number) + vertical_shift,
                buff = 0,
                color = color_list[0],
            )
            arrow.start_number = start_number
            arrow.end_number = end_number
            arrow.vertical_shift = vertical_shift
            arrow.add_updater(set_start_end_arrow)
            exp_arrows.append(arrow)
        

        m1_arrows = []
        for i in positive_power_list[:-1]:
            for j in range(2):
                start_number = 2**i*(1 + j/2)
                end_number = 2**i*(1 + (j+1)/2)
                vertical_shift = 2*DOWN*0.5
                arrow = DoubleArrow(
                    start = self.real_line.n2p(start_number) + vertical_shift,
                    end = self.real_line.n2p(end_number) + vertical_shift,
                    buff = 0,
                    color = color_list[1],
                )
                arrow.start_number = start_number
                arrow.end_number = end_number
                arrow.vertical_shift = vertical_shift
                arrow.add_updater(set_start_end_arrow)
                m1_arrows.append(arrow)

        m2_arrows = []
        for i in positive_power_list[:-1]:
            for j in range(4):
                start_number = 2**i*(1 + j/4)
                end_number = 2**i*(1 + (j+1)/4)
                vertical_shift = 3*DOWN*0.5
                arrow = DoubleArrow(
                    start = self.real_line.n2p(start_number) + vertical_shift,
                    end = self.real_line.n2p(end_number) + vertical_shift,
                    buff = 0,
                    color = color_list[2],
                )
                arrow.start_number = start_number
                arrow.end_number = end_number
                arrow.vertical_shift = vertical_shift
                arrow.add_updater(set_start_end_arrow)
                m2_arrows.append(arrow)

        m3_arrows = []
        for i in positive_power_list[6:-1]:
            for j in range(8):
                start_number = 2**i*(1 + j/8)
                end_number = 2**i*(1 + (j+1)/8)
                vertical_shift = 4*DOWN*0.5
                arrow = DoubleArrow(
                    start = self.real_line.n2p(start_number) + vertical_shift,
                    end = self.real_line.n2p(end_number) + vertical_shift,
                    buff = 0,
                    color = color_list[3],
                )
                arrow.start_number = start_number
                arrow.end_number = end_number
                arrow.vertical_shift = vertical_shift
                arrow.add_updater(set_start_end_arrow)
                m3_arrows.append(arrow)

        m4_arrows = []
        for i in positive_power_list[7:-1]:
            for j in range(16):
                start_number = 2**i*(1 + j/16)
                end_number = 2**i*(1 + (j+1)/16)
                vertical_shift = 5*DOWN*0.5
                arrow = DoubleArrow(
                    start = self.real_line.n2p(start_number) + vertical_shift,
                    end = self.real_line.n2p(end_number) + vertical_shift,
                    buff = 0,
                    color = color_list[4],
                )
                arrow.start_number = start_number
                arrow.end_number = end_number
                arrow.vertical_shift = vertical_shift
                arrow.add_updater(set_start_end_arrow)
                m4_arrows.append(arrow)

        def set_start_end_boundary(mobj):
            mobj.put_start_and_end_on(
                self.real_line.n2p(mobj.start_number),
                self.real_line.n2p(mobj.start_number) + mobj.len,
            )
        boundaries = []
        for i in positive_power_list:
            boundary = four_boundary.copy()
            boundary.start_number = 2**i
            boundary.len = boundary_length*DOWN/3
            boundary.add_updater(set_start_end_boundary)
            boundaries.append(boundary)
        
        self.play(
            ReplacementTransform(four_boundary, boundaries[3]),
            ReplacementTransform(eight_boundary, boundaries[4]),
            ReplacementTransform(sixteen_boundary, boundaries[5]),

            ReplacementTransform(exp_arr_pow2, exp_arrows[3]),
            FadeOut(exp_arr_pow2_gv.submobjects[1]),
            ReplacementTransform(exp_arr_pow3, exp_arrows[4]),
            FadeOut(exp_arr_pow3_gv.submobjects[1]),

            ReplacementTransform(m1_arr_pow2_gv.submobjects[0], m1_arrows[6]),
            ReplacementTransform(m1_arr_pow2_gv.submobjects[1], m1_arrows[7]),
            FadeOut(*m1_arr_pow2_gv.submobjects[2:]),
            ReplacementTransform(m1_arr_pow3_gv.submobjects[0], m1_arrows[8]),
            ReplacementTransform(m1_arr_pow3_gv.submobjects[1], m1_arrows[9]),
            FadeOut(*m1_arr_pow3_gv.submobjects[2:]),

            ReplacementTransform(m2_arr_pow2_gv.submobjects[0], m2_arrows[12]),
            ReplacementTransform(m2_arr_pow2_gv.submobjects[1], m2_arrows[13]),
            ReplacementTransform(m2_arr_pow2_gv.submobjects[2], m2_arrows[14]),
            ReplacementTransform(m2_arr_pow2_gv.submobjects[3], m2_arrows[15]),
            FadeOut(*m2_arr_pow2_gv.submobjects[4:]),
            ReplacementTransform(m2_arr_pow3_gv.submobjects[0], m2_arrows[16]),
            ReplacementTransform(m2_arr_pow3_gv.submobjects[1], m2_arrows[17]),
            ReplacementTransform(m2_arr_pow3_gv.submobjects[2], m2_arrows[18]),
            ReplacementTransform(m2_arr_pow3_gv.submobjects[3], m2_arrows[19]),
            FadeOut(*m2_arr_pow3_gv.submobjects[4:]),

            FadeIn(*boundaries[6:]),
            FadeIn(*exp_arrows[5:], shift  = UP ),
            FadeIn(*m1_arrows[10:], shift = UP),
            FadeIn(*m2_arrows[20:], shift = UP),
            FadeIn(*m3_arrows, shift = UP),
            FadeIn(*m4_arrows, shift = UP),
        )
        
        A = 8.0
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )
        self.play(
            self.real_line.animate.scale(
                0.5, about_point = self.real_line.n2p(8)
            ).shift(
                LEFT*np.linalg.norm(self.real_line.n2p(8)-self.real_line.n2p(4))
            )
        )

        A = 16.0 - (16/4)
        
        self.common_mantissa_bits = 2
        new_frame_common_mantissa_bits = Rectangle(
            width = np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n1[self.common_mantissa_bits].get_vertices()[0]),
            height = rect_size[0] + np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n2[0].get_vertices()[0]),
            color = RED,
            stroke_width = 8
        ).move_to(
            (mantissa_blocks_n1[0].get_center() + mantissa_blocks_n2[self.common_mantissa_bits-1].get_center())/2.0
        )
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )
        self.play(Transform(frame_common_mantissa_bits,new_frame_common_mantissa_bits))
        self.play(
            self.real_line.animate.scale(
                0.5, about_point = self.real_line.n2p(16)
            ).shift(
                LEFT*np.linalg.norm(self.real_line.n2p(16)-self.real_line.n2p(8))
            ),
            
        )

        A = 32.0 - (32/8)
        
        self.common_mantissa_bits = 3
        new_frame_common_mantissa_bits = Rectangle(
            width = np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n1[self.common_mantissa_bits].get_vertices()[0]),
            height = rect_size[0] + np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n2[0].get_vertices()[0]),
            color = RED,
            stroke_width = 8
        ).move_to(
            (mantissa_blocks_n1[0].get_center() + mantissa_blocks_n2[self.common_mantissa_bits-1].get_center())/2.0
        )
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )
        self.play(Transform(frame_common_mantissa_bits,new_frame_common_mantissa_bits))
        self.play(
            self.real_line.animate.scale(
                0.5, about_point = self.real_line.n2p(32)
            ).shift(
                LEFT*np.linalg.norm(self.real_line.n2p(32)-self.real_line.n2p(16))
            ),
            
        )
        A = 64.0 - (64/16)
        
        self.common_mantissa_bits = 4
        new_frame_common_mantissa_bits = Rectangle(
            width = np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n1[self.common_mantissa_bits].get_vertices()[0]),
            height = rect_size[0] + np.linalg.norm(mantissa_blocks_n1[0].get_vertices()[0] - mantissa_blocks_n2[0].get_vertices()[0]),
            color = RED,
            stroke_width = 8
        ).move_to(
            (mantissa_blocks_n1[0].get_center() + mantissa_blocks_n2[self.common_mantissa_bits-1].get_center())/2.0
        )
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=1,
        )

        self.play(Transform(frame_common_mantissa_bits,new_frame_common_mantissa_bits))
        # self.play(
        #     self.real_line.animate.scale(
        #         0.5, about_point = self.real_line.n2p(32)
        #     ).shift(
        #         LEFT*np.linalg.norm(self.real_line.n2p(32)-self.real_line.n2p(16))
        #     ),
            
        # )
        
        self.camera.frame.save_state()
        ##SHOW WHAT HAPPENS IN TERMS OF ERROR
        self.play(
            self.camera.frame.animate.scale(0.2).move_to(x_fp_exp2),
            FadeOut(y_fp_exp2),
            FadeOut(y_fp_exp2_label),
            FadeOut(plus_A_line),
        )
        new_real_line = self.real_line.copy()
        new_real_line.x_range[2] = 8.0
        new_real_line.set(
            tick_size = 0.2,
            unit = 8.0
        ).add_ticks()
    

        self.play(
            Write(new_real_line)
            #Transform(self.real_line, new_real_line)
        )
        self.real_line.become(new_real_line)
        self.remove(new_real_line)

        def move_x_point(mobj):
            mobj.move_to(x_fp_exp2.get_center())

        self.camera.frame.add_updater(move_x_point)
        A = 65.4
        self.remove(title_of_the_paper)
        self.add(title_of_the_paper)
        self.play(
            self.x_fp.animate.increment_value(A),
            self.y_fp.animate.increment_value(A),
            run_time=5,
        )
        
        x_fp_exp2_true = x_fp_exp2.copy().set(color = "#d62828").clear_updaters()
        x_fp_exp2_label_true = MathTex(
            r"{{x}}^*").set(
            color = "#d62828").move_to(
            x_fp_exp2_label, aligned_edge = LEFT + DOWN)
        self.play(FadeIn(x_fp_exp2_true, x_fp_exp2_label_true))

        self.play(
            self.x_fp.animate.set_value(np.floor(self.x_fp.get_value()/8.0)*8.0),
            self.y_fp.animate.set_value(np.floor(self.x_fp.get_value()/8.0)*8.0),
            run_time=1,
        )

        # delta_arrow_forward = DoubleArrow(
        #     buff = 0,
        #     max_tip_length_to_length_ratio=0.2,
        #     start = x_fp_exp2.get_center() + DOWN*0.1,
        #     end = x_fp_exp2_true.get_center()+ DOWN*0.1,
        #     color = "#d62828"
        # )
        delta_arrow_forward = Line(
            start = x_fp_exp2.get_center(),
            end = x_fp_exp2_true.get_center(),
            color = "#d62828"
        )
        delta_arrow_forward_label = MathTex(
            r"\Delta_x",
            font_size = 40,
            color = "#d62828"
        ).next_to(delta_arrow_forward, DOWN*0.1)

        self.play(
            FadeIn(
                delta_arrow_forward,
                delta_arrow_forward_label
            ),
            run_time=1,
        )
        
        self.play(
            self.x_fp.animate.increment_value(-A-0.8),
            self.y_fp.animate.increment_value(-A-0.8),
            run_time=5,
        )
        x_fp_exp2_true_backward = x_fp_exp2.copy().set(color = "#005f73").clear_updaters()
        x_fp_exp2_label_backward_true = MathTex(
            r"{{x}}^*").set(
            color = "#005f73").move_to(x_fp_exp2_label, aligned_edge = LEFT + DOWN)
        self.play(FadeIn(x_fp_exp2_true_backward, x_fp_exp2_label_backward_true))


        self.play(
            self.x_fp.animate.set_value(np.floor(self.x_fp.get_value()/8.0)*8.0 + 8.0),
            self.y_fp.animate.set_value(np.floor(self.x_fp.get_value()/8.0)*8.0 + 8.0),
            run_time=1,
        )

        delta_arrow_backward = Line(
            start = x_fp_exp2.get_center(),
            end = x_fp_exp2_true_backward.get_center(),
            color = "#005f73"
        )
        delta_arrow_backward_label = MathTex(
            r"\Delta_x",
            font_size = 40,
            color = "#005f73"
        ).next_to(delta_arrow_backward, DOWN*0.1)



        self.play(
            FadeIn(
                delta_arrow_backward,
                delta_arrow_backward_label
            ),
            run_time=1,
        )
        self.camera.frame.remove_updater(move_x_point)
        self.play(
            self.camera.frame.animate.scale(3.5).move_to(
                self.real_line.n2p(145)+3.0*UP
            ),
        )
        #self.play(Restore(self.camera.frame))

        
        ### ORIGINAL DATASET

        addition_all_objects = VGroup()

        center_of_image = self.camera.frame_center
        original_x_ds_vg = VGroup(*[
            MathTex(
                r"{{x}}_{{{}}}".format(i)
            ).move_to(center_of_image + 0.5 *UP)
            for i in range(5)
        ])
        original_x_ds_vg.arrange_in_grid(rows = 5, cols = 1, buff = 0.8)
        framebox_original = Rectangle(
            color = BLACK,
            height = original_x_ds_vg.height + 0.5, 
            width = original_x_ds_vg.width + 0.5,
        ).move_to(original_x_ds_vg.get_center())

        addition_all_objects += original_x_ds_vg
        addition_all_objects += framebox_original

        addition_all_objects.move_to(
                center_of_image+ 0.5*UP
        )
        self.play(
            Write(original_x_ds_vg),
            Create(framebox_original),
        )

        ## MOD DATASET
        self.play(addition_all_objects.animate.shift(
            2*LEFT
            )
        )
        arrow_plus_A = Arrow(
            stroke_width = 10,
            color = BLACK
        ).next_to(
            framebox_original,
            RIGHT,
            buff = .2
        )
        arrow_plus_A_label = MathTex("+A").next_to(
            arrow_plus_A, UP, buff = 0.2
        )
        mod_x_ds = []
        for i in range(5):
            x = MathTex(
                r"x_{} + A + \Delta_{{x_{}}}".format(str(i), str(i))
            )
            x.next_to(arrow_plus_A, RIGHT, buff = .4)
            x[0][5:].set(color = "#d62828")
            mod_x_ds.append(x)
        mod_x_ds_vg = VGroup(*mod_x_ds)
        mod_x_ds_vg.arrange_in_grid(rows = 5, cols = 1, buff = 0.05)
        framebox_mod = Rectangle(
            color = "#d62828",
            height = mod_x_ds_vg.height + 0.5, 
            width = mod_x_ds_vg.width + 0.5,
        ).move_to(mod_x_ds_vg.get_center())

        addition_all_objects.add(
            arrow_plus_A,
            arrow_plus_A_label,
            mod_x_ds_vg,
            framebox_mod
        )
        self.play(
            AnimationGroup(   
                GrowArrow(arrow_plus_A),
                Write(arrow_plus_A_label),
                Write(mod_x_ds_vg),
                Create(framebox_mod),
                lag_ratio=0.2,
            )
        )
        
        ## RECOVERED DATASET
        self.play(addition_all_objects.animate.shift(
            3.5*LEFT 
            )
        )
        arrow_minus_A = Arrow(
            stroke_width = 10,
            color = BLACK
        ).next_to(
            framebox_mod,
            RIGHT,
            buff = .2
        )
        arrow_minus_A_label = MathTex("-A").next_to(
            arrow_minus_A, UP, buff = 0.2
        )
        rec_x_ds = []
        for i in range(5):
            x = MathTex(
                r"x_{} + \Delta_{{x_{}}} + \Delta_{{x_{}}} ".format(str(i), str(i), str(i))
            )
            x.next_to(arrow_minus_A,  RIGHT, buff = .4)
            x[0][3:6].set(color = "#d62828")
            x[0][7:].set(color = "#005f73")
            rec_x_ds.append(x)
        rec_x_ds_vg = VGroup(*rec_x_ds)
        rec_x_ds_vg.arrange_in_grid(rows = 5, cols = 1, buff = 0.5)
        framebox_rec = Rectangle(
            color = "#005f73",
            height = framebox_original.height, 
            width = rec_x_ds_vg.width + 0.5,
        ).move_to(rec_x_ds_vg.get_center())
        
        self.play(
            AnimationGroup(   
                GrowArrow(arrow_minus_A),
                Write(arrow_minus_A_label),
                Write(rec_x_ds_vg),
                Create(framebox_rec),
                lag_ratio=0.2,
            )
        )
        addition_all_objects.add(
            arrow_minus_A,
            arrow_minus_A_label,
            rec_x_ds_vg,
            framebox_rec
        )
        self.wait(1)

    def __init__(
        self,
        var: float,
        label: str | Tex | MathTex | Text | SingleStringMathTex,
        var_type: DecimalNumber | Integer = DecimalNumber,
        num_decimal_places: int = 2,
        **kwargs,
    ):
        self.label = MathTex(label) if isinstance(label, str) else label
        equals = MathTex("=").next_to(self.label, RIGHT)
        self.label.add(equals)

class MultiplicationMethod(Scene):
    #config["frame_rate"] = 30
    def construct(self): 
        def place_at_the_top_of_frame(mobj):
            mobj.move_to(self.camera.frame_center + UP*(self.camera.frame_height/2)*0.9 )
            mobj.rescale_to_fit(self.camera.frame_width*0.8, 0)
            mobj.underline.set_stroke(width = self.camera.frame_height/10)
        title_of_the_paper = Title(
            f"Change a bit to save a byte, Francesco Taurone et al.",
            stroke_color = BLACK,
            font_size = 40,
            underline_buff=SMALL_BUFF
        ).add_updater(place_at_the_top_of_frame)
        title_of_the_paper.underline.set_color(BLACK)
        title_of_the_paper.set_color(BLACK)
        self.add(title_of_the_paper) 
        def write_mantissa(mobj):
            x_fp_mantissa = su.getLongIntFromSingleMantissa(mobj.x_fp.get_value())
            mantissa = "1."+(bin(x_fp_mantissa)[2:].rjust(23, "0"))
            mobj.set_value(np.double(mantissa))
        self.camera.background_color = "#edf2f4"
        number_dict = {
            3: 5.0, #1.667
            7: 19.0, #2.714
            13: 27.0, #2.077  
        }
        Text.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        start = 1.000
        num_decimal_places = 3 

        x_var_tr = ValueTracker(start)

        x_title = MathTex("x")
        x_times_3_title = MathTex("x \cdot 3")
        x_times_7_title = MathTex("x \cdot 7")
        x_times_13_title = MathTex("x \cdot 13")

        x_var_dec = DecimalNumber(
            start, num_decimal_places=num_decimal_places
        ).add_updater(lambda v: v.set_value(x_var_tr.get_value()), call_updater=True)
        x_var_dec.set(color = BLACK)
        self.x_times_3_var_dec = DecimalNumber(
            start*3, num_decimal_places=num_decimal_places
        ).add_updater(lambda v: v.set_value(x_var_tr.get_value()*3.0), call_updater=True)
        self.x_times_3_var_dec.set(color = BLACK)
        self.x_times_7_var_dec = DecimalNumber(
            start*7, num_decimal_places=num_decimal_places
        ).add_updater(lambda v: v.set_value(x_var_tr.get_value()*7.0), call_updater=True)
        self.x_times_7_var_dec.set(color = BLACK)
        self.x_times_13_var_dec = DecimalNumber(
            start*13, num_decimal_places=num_decimal_places
        ).add_updater(lambda v: v.set_value(x_var_tr.get_value()*13.0), call_updater=True)
        self.x_times_13_var_dec.set(color = BLACK)
        

        # 3

        # def write_result_3(mobj):
        #     control = self.x_times_3_var_dec.get_value()
        #     if int(control) == control:
        #         mobj.set_value(control)
        #         mobj.set(color = BLACK)
            
        result_3_x = MathTex(
            r"1.667",
            color = self.camera.background_color,
        )#.add_updater(write_result_3)
        result_3_y = MathTex(
            r"5.000",
            color = self.camera.background_color,
        )
        # 13
            
        result_13_x = MathTex(
            r"2.077",
            color = self.camera.background_color,
        )
        result_13_y = MathTex(
            r"27.000",
            color = self.camera.background_color,
        )

        # 7
            
        result_7_x = MathTex(
            r"2.714",
            color = self.camera.background_color,
        )
        result_7_y = MathTex(
            r"19.000",
            color = self.camera.background_color,
        )
        multiply_3 = MathTex("M = 3")
        multiply_7 = MathTex("M = 7")
        multiply_13 = MathTex("M = 13")

        variables = VGroup(
            MathTex(""), x_title, x_times_3_title,x_times_7_title,x_times_13_title,
            MathTex(""), x_var_dec, self.x_times_3_var_dec,self.x_times_7_var_dec, self.x_times_13_var_dec,
            multiply_3,result_3_x,result_3_y,MathTex(""),MathTex(""),
            multiply_7,result_7_x,MathTex(""),result_7_y,MathTex(""),
            multiply_13,result_13_x,MathTex(""),MathTex(""),result_13_y,
            #Tex("Mantissa"), x_var_mantissa,x_times_3_mantissa,

        )
        variables.arrange_in_grid(
            rows = 5, cols = 5, col_alignments="rcccc", flow_order="rd",
            buff = (0.6, 0.4)
        )
        variables.move_to(self.camera.frame_center)

        self.add(*variables)
        
        #X
        rectangle_x = SurroundingRectangle(x_var_dec, color = BLACK)
        self.play(
            Create(rectangle_x),
        )
        
        #3
        self.play(x_var_tr.animate.set_value(5/3.0), run_time=2, rate_func=linear)
        rectangle_3_x = SurroundingRectangle(result_3_x, color = GREEN)
        rectangle_3_y = SurroundingRectangle(result_3_y, color = GREEN)
        self.play(
            FadeToColor(result_3_x, BLACK),
            FadeToColor(result_3_y, BLACK),
            Create(rectangle_3_x),
            Create(rectangle_3_y)
        )

        #13
        self.play(x_var_tr.animate.set_value(27.0/13.0), run_time=2, rate_func=linear)
        rectangle_13_x = SurroundingRectangle(result_13_x, color = ORANGE)
        rectangle_13_y = SurroundingRectangle(result_13_y, color = ORANGE)
        self.play(
            FadeToColor(result_13_x, BLACK),
            FadeToColor(result_13_y, BLACK),
            Create(rectangle_13_x),
            Create(rectangle_13_y)
        )

        #7
        self.play(x_var_tr.animate.set_value(19.0/7.0), run_time=2, rate_func=linear)
        rectangle_7_x = SurroundingRectangle(result_7_x, color = BLUE)
        rectangle_7_y = SurroundingRectangle(result_7_y, color = BLUE)
        self.play(
            FadeToColor(result_7_x, BLACK),
            FadeToColor(result_7_y, BLACK),
            Create(rectangle_7_x),
            Create(rectangle_7_y),
        )

        #MANTISSAS
        self.play(
            FadeOut(x_times_3_title,x_times_7_title,x_times_13_title,),
            FadeOut(self.x_times_3_var_dec,self.x_times_7_var_dec, self.x_times_13_var_dec,),

            VGroup(
                x_title, x_var_dec,rectangle_x,
                multiply_3, multiply_7, multiply_13,
                result_3_x, result_7_x, result_13_x,
                rectangle_3_x,rectangle_7_x,rectangle_13_x,

            ).animate.shift(2*LEFT),

            Transform(result_3_y, result_3_y.copy().align_to(result_13_y, RIGHT)),
            Transform(result_7_y, result_7_y.copy().align_to(result_13_y, RIGHT)),
            Transform(result_13_y, result_13_y.copy().align_to(result_13_y, RIGHT)),
            Transform(rectangle_3_y, rectangle_3_y.copy().align_to(rectangle_13_y, RIGHT)),
            Transform(rectangle_7_y, rectangle_7_y.copy().align_to(rectangle_13_y, RIGHT)),
            Transform(rectangle_13_y, rectangle_13_y.copy().align_to(rectangle_13_y, RIGHT)),
        )
        mantissa_title = Tex("x Mantissa").align_to(x_title, UP)
        x_times_3_mantissa = MathTex("1.\overline{10}").align_to(rectangle_3_x, UP)
        x_times_3_mantissa.set(color = BLACK)
        x_times_3_mantissa[0][2].set_color(GREEN)

        x_times_7_mantissa = MathTex("1.01\overline{011}").align_to(rectangle_7_x, UP)
        x_times_7_mantissa.set(color = BLACK)
        x_times_7_mantissa[0][4].set_color(BLUE)

        x_times_13_mantissa = MathTex("1.0\overline{000100111011}").align_to(rectangle_13_x, UP)
        x_times_13_mantissa.set(color = BLACK)
        x_times_13_mantissa[0][3].set_color(ORANGE)

        self.play(
            AnimationGroup(
                Write(mantissa_title),
                Write(x_times_3_mantissa),
                Write(x_times_7_mantissa),
                Write(x_times_13_mantissa),
                lag_ratio=0.2
            )
            
        )
        self.wait()
        
        #Dataset

        ds_title = Tex("Dataset").next_to(x_title, LEFT, buff = 2*MED_LARGE_BUFF)
        x_ds_3 = MathTex("1.652").next_to(rectangle_3_x, LEFT).align_to(ds_title, LEFT)
        x_ds_7 = MathTex("2.651").next_to(rectangle_7_x, LEFT).align_to(ds_title, LEFT)
        x_ds_13 = MathTex("2.071").next_to(rectangle_13_x, LEFT).align_to(ds_title, LEFT)
        self.play(
            Write(ds_title),
            ReplacementTransform(multiply_3, x_ds_3),
            ReplacementTransform(multiply_7, x_ds_7),
            ReplacementTransform(multiply_13, x_ds_13),
        )

class Compression(MovingCameraScene):
    def construct(self):
        def place_at_the_top_of_frame(mobj):
            mobj.move_to(self.camera.frame_center + UP*(self.camera.frame_height/2)*0.9 )
            mobj.rescale_to_fit(self.camera.frame_width*0.8, 0)
            mobj.underline.set_stroke(width = self.camera.frame_height/10)
        title_of_the_paper = Title(
            f"Change a bit to save a byte, Francesco Taurone et al.",
            stroke_color = BLACK,
            font_size = 40,
            underline_buff=SMALL_BUFF
        ).add_updater(place_at_the_top_of_frame)
        title_of_the_paper.underline.set_color(BLACK)
        title_of_the_paper.set_color(BLACK)
        self.add(title_of_the_paper) 
        self.camera.background_color = "#edf2f4"
        MathTex.set_default(color=BLACK)
        shared_sequence = "100010111"
        line1 = MathTex(r"1010010", r"{{{}}}".format(shared_sequence))
        line2 = MathTex(r"0001001", r"{{{}}}".format(shared_sequence))
        line3 = MathTex(r"0010111", r"{{{}}}".format(shared_sequence))
        line4 = MathTex(r"1010011", r"{{{}}}".format(shared_sequence))
        line5 = MathTex(r"1111100", r"{{{}}}".format(shared_sequence))
        line6 = MathTex(r"0001100", r"{{{}}}".format(shared_sequence))
        lines = VGroup(
            line1, line2, line3,
            line4, line5, line6,
        )
        lines.arrange(direction=DOWN, buff=0.1)
        self.add(*lines.submobjects)
        frame = Rectangle(
            width = lines.width + SMALL_BUFF,
            height = lines.height+ SMALL_BUFF,
            color = BLACK
        ).move_to(
            lines.get_center()
        )
        self.add(frame)
        #self.camera.frame.set(width=line1.width * 1.2)
        self.camera.frame.scale(0.5)
        self.play(
            #self.camera.frame.animate.scale(0.5)
            AnimationGroup(*[
                FadeToColor(line[1], RED)#[-len(shared_sequence):], RED)
                    for line in lines
                ]
            ),
        )
        last_line = MathTex(
            r"\star = {{{}}}".format(shared_sequence),
            color = RED
        ).next_to(
            line6, DOWN , buff=0.1
        ).align_to(
            line6,LEFT 
        )

        transformed_lines = [
            MathTex(
                    r"1010010", r"\star"
            ),
            MathTex(
                    r"0001001", r"\star"
            ),
            MathTex(
                    r"0010111", r"\star"
            ),
            MathTex(
                    r"1010011", r"\star"
            ),
            MathTex(
                    r"1111100", r"\star"
            ),
            MathTex(
                    r"0001100", r"\star"
            ),
        ]
        transformed_lines_vg = VGroup(*transformed_lines)

        for line in transformed_lines:
            line[1].set(color = RED)
        self.play(
            Write(last_line),
            TransformMatchingTex(
                line1, transformed_lines[0].move_to(line1.get_center()).align_to(line1, LEFT)
            ),
            TransformMatchingTex(
                line2, transformed_lines[1].move_to(line2.get_center()).align_to(line2, LEFT)
            ),
            TransformMatchingTex(
                line3, transformed_lines[2].move_to(line3.get_center()).align_to(line3, LEFT)
            ),
            TransformMatchingTex(
                line4, transformed_lines[3].move_to(line4.get_center()).align_to(line4, LEFT)
            ),
            TransformMatchingTex(
                line5, transformed_lines[4].move_to(line5.get_center()).align_to(line5, LEFT)
            ),
            TransformMatchingTex(
                line6, transformed_lines[5].move_to(line6.get_center()).align_to(line6, LEFT)
            )
        )
        self.play(
            Transform(
                frame, 
                Rectangle(
                    width = transformed_lines_vg.width + SMALL_BUFF,
                    height = transformed_lines_vg.height+ SMALL_BUFF,
                    color = BLACK
                ).move_to(
                    transformed_lines_vg.get_center()
                )
            ),
            Write(
                Rectangle(
                    width = last_line.width + SMALL_BUFF,
                    height = last_line.height+ SMALL_BUFF,
                    color = RED
                ).move_to(
                    last_line.get_center()
                )
            )
        )   
        #self.camera.auto_zoom(mobjects = lines.submobjects, animate = False)
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title_of_the_paper]
            # All mobjects in the screen are saved in self.mobjects
        )

class Results(MovingCameraScene):
    def construct(self):
        def place_at_the_top_of_frame(mobj):
            mobj.move_to(self.camera.frame_center + UP*(self.camera.frame_height/2)*0.9 )
            mobj.rescale_to_fit(self.camera.frame_width*0.8, 0)
            mobj.underline.set_stroke(width = self.camera.frame_height/10)
        title_of_the_paper = Title(
            f"Change a bit to save a byte, Francesco Taurone et al.",
            stroke_color = BLACK,
            font_size = 40,
            underline_buff=SMALL_BUFF
        ).add_updater(place_at_the_top_of_frame)
        title_of_the_paper.underline.set_color(BLACK)
        title_of_the_paper.set_color(BLACK)
        self.add(title_of_the_paper) 
        self.camera.background_color = "#edf2f4"
        MathTex.set_default(color=BLACK)

        ax = Axes(
            x_range = [0, 1, 0.2],
            y_range = [-80, 10, 10],
            axis_config={
                "include_tip": False,
                "font_size": 24,
                "include_numbers": True,
                "color": BLACK,
                "label_direction":UP,
            },
            x_length = 0.3*self.camera.frame.width,
            y_length = 0.6*self.camera.frame.height,
        ).add_coordinates()
        ax.x_axis.numbers.set(color = BLACK)
        ax.y_axis.numbers.set(color = BLACK)
        ax.center()
        y_label = ax.get_y_axis_label(
            Tex("Dataset Size Reduction (\%)").scale(0.65).rotate(90 * DEGREES),
            edge=LEFT, direction=LEFT, buff = 0.4
        )
        x_label = ax.get_x_axis_label(
            Tex("Max Error(\%)").scale(0.65),
            edge=RIGHT, direction=LEFT, buff=-0.4
        ).shift(1.8*RIGHT)
        self.play(
            Write(ax),
            FadeIn(y_label, x_label)
        )
        dashed_lines = VGroup()
        for x in np.arange(0.2, 1.2, 0.2):
            dashed_lines.add(
                ax.get_vertical_line(
                    ax.coords_to_point(x,-80),
                    line_config={
                        "dashed_ratio": 0.55,
                        "stroke_color":GREY,
                    }
                )
            )
        
        for y in np.arange(-80, 10, 10):
            dashed_lines.add(
                ax.get_horizontal_line(
                    ax.coords_to_point(1,y),
                    line_config={
                        "dashed_ratio": 0.55,
                        "stroke_color":GREY,
                    }
                )
            )
        self.play(
            Write(dashed_lines)
        )
        #ax.set(color = BLACK)
        
        dot_config = {
            "radius" : DEFAULT_DOT_RADIUS*2.0,
            "fill_opacity":0.5,
            "stroke_width": 2.0,
            "stroke_color":BLACK,
        }
        star_config = {
            "outer_radius":DEFAULT_DOT_RADIUS*3.0,
            "stroke_color": BLACK,
            "fill_opacity":0.5,
            "stroke_width": 2.0,
        }
        # CBB
        dot_add_cbb = [
            Dot(
                ax.coords_to_point(1, -33),
                fill_color = GREEN,
                **dot_config,
            ),
            Dot(
                ax.coords_to_point(0.2, -21),
                fill_color = GREEN,
                **dot_config,
            ),
            Dot(
                ax.coords_to_point(0.01, -8),
                fill_color = GREEN,
                **dot_config,
            ),
        ]
        star_add_cbb = [
            Star(
                fill_color = GREEN,
                **star_config
            ).move_to(
                ax.coords_to_point(0.13, 0.0)
            )
        ]
        triangle_add_cbb = [
            Triangle(
                fill_color = GREEN, 
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.97, -36)
            ),
            Triangle(
                fill_color = GREEN,
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.12, -8)
            ),
            Triangle(
                fill_color = GREEN,
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.03, 3)
            ),
        ]
        # CBB_dim2
        dot_add_cbb_dim2 = [
            Dot(
                ax.coords_to_point(0.9, -54),
                fill_color = RED,
                **dot_config,
            ),
            Dot(
                ax.coords_to_point(0.342, -48.3),
                fill_color = RED,
                **dot_config,
            ),
            Dot(
                ax.coords_to_point(0.14, -38.8),
                fill_color = RED,
                **dot_config,
            ),
        ]
        triangle_add_cbb_dim2 = [
            Triangle(
                fill_color = RED, 
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(1, -80)
            ),
            Triangle(
                fill_color = RED,
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.61, -65.3)
            ),
            Triangle(
                fill_color = RED,
                **dot_config
            ).rotate(60*DEGREES).scale(1.2).move_to(
                ax.coords_to_point(0.13, -49.3)
            )
        ]
        star_add_cbb_dim2 = [
            Star(
                fill_color = RED,
                **star_config
            ).move_to(
                ax.coords_to_point(0.72, -48.1)
            ),
            Star(
                fill_color = RED,
                **star_config
            ).move_to(
                ax.coords_to_point(0.38, -42.5)
            ),
            Star(
                fill_color = RED,
                **star_config
            ).move_to(
                ax.coords_to_point(0.017, -22.1)
            ),
        ]
        ## LEGEND
        legend_color = Tex(
            "COLORS: Datasets",
            font_size = 30
        )
        legend_triangle = Triangle(
            radius=DEFAULT_DOT_RADIUS*2.0,
            color= GREEN,
            fill_opacity=0.5,
            stroke_width= 2.0,
            stroke_color=BLACK,
            fill_color=self.camera.background_color,
        ).rotate(60*DEGREES).scale(1.2).next_to(legend_color, DOWN).shift(LEFT)
        legend_triangle_desc = Tex(
            ": Multiplication",
            font_size = 30
        ).next_to(legend_triangle, RIGHT)
        legend_dot = Dot(
            radius=DEFAULT_DOT_RADIUS*2.0,
            color= GREEN,
            fill_opacity=0.5,
            stroke_width= 2.0,
            stroke_color=BLACK,
            fill_color=self.camera.background_color,
        ).next_to(legend_color, 2.5*DOWN).shift(LEFT)
        legend_dot_desc = Tex(
            ": Addition",
            font_size = 30
        ).next_to(legend_dot, RIGHT)
        legend_star = Star(
            outer_radius=DEFAULT_DOT_RADIUS*3.0,
            color= GREEN,
            fill_opacity=0.5,
            stroke_width= 2.0,
            stroke_color=BLACK,
            fill_color=self.camera.background_color,
        ).next_to(legend_color, 4*DOWN).shift(LEFT)
        legend_star_desc = Tex(
            ": Info",
            font_size = 30
        ).next_to(legend_star, RIGHT)
        legend_tot = VGroup(
            legend_color,
            legend_triangle,
            legend_triangle_desc,
            legend_dot,
            legend_dot_desc,
            legend_star,
            legend_star_desc,
        ).align_on_border(RIGHT)


        self.play(
            FadeIn(legend_tot),
        )
        
        self.play(
            AnimationGroup(
                FadeIn(*dot_add_cbb,scale=1.5),
                FadeIn(*star_add_cbb,scale=1.5),
                FadeIn(*triangle_add_cbb,scale=1.5),
                lag_ratio=0.2,
            )
        )
        self.play(
            AnimationGroup(
                FadeIn(*dot_add_cbb_dim2,scale=1.5),
                FadeIn(*star_add_cbb_dim2,scale=1.5),
                FadeIn(*triangle_add_cbb_dim2,scale=1.5),
                lag_ratio=0.2,
            )
        )
        self.wait()