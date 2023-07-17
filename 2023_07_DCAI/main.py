from manim import *
from manim_slides import Slide
import os
sys.path.insert(0, os.path.abspath(".."))
import numpy as np
import struct

def getBitsForFloat16(fpNumber):
    data = struct.pack("!e", fpNumber)
    return bin(struct.unpack("!h", data)[0])[2:].rjust(16, "0")

def deduplication(self):
    
    self.camera.frame.scale(0.5)
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
    lines.arrange(direction=DOWN, buff=0.1).move_to(self.camera.frame.get_center())
    self.play(
        Write(lines)
    )
    frame = Rectangle(
        width = lines.width + SMALL_BUFF,
        height = lines.height+ SMALL_BUFF,
        color = BLACK
    ).move_to(
        lines.get_center()
    )
    self.play(Create(frame))
    #self.camera.frame.set(width=line1.width * 1.2)
    
    self.play(
        #self.camera.frame.animate.scale(0.5)
        AnimationGroup(*[
            FadeToColor(line[1], RED)#[-len(shared_sequence):], RED)
                for line in lines
            ]
        ),
    )
    self.wait(0.1)
    self.next_slide()
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
    self.wait(0.1)
    self.next_slide()
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
    self.wait(0.1)
    self.next_slide()
    self.play(
        *[FadeOut(mob) for mob in self.mobjects if mob != self.title_of_the_paper]
        # All mobjects in the screen are saved in self.mobjects
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        Restore(self.camera.frame)
    )
    self.wait(0.1)
    self.next_slide()

def compression (self):
    ###COMPRESSION
        data_points=VGroup(
            *[
                Rectangle(
                    height = 1.0,
                    width = 1.2,
                    #fill_opacity = 0.5,
                    color = rgb_to_color(np.random.rand(3)*color_to_rgb(self.color_list[0]))
                ) for _ in range(0,30)
            ]
        )
        data_points.arrange_in_grid(rows=5, buff=0.15)

        self.play(
            AnimationGroup(
                *[FadeIn(datum) for datum in data_points],
                lag_ratio=0.1,
            )
        )
        self.wait(0.1)
        self.next_slide()
        data_points.save_state() 
        self.play(
            AnimationGroup(
                *[
                    datum.animate.move_to(self.camera.frame_center)
                    for datum in data_points
                ],
                lag_ratio = 0.05
            )
        )
        self.wait(0.1)
        self.next_slide()
        self.play(
            AnimationGroup(
                Restore(data_points),
            )
        )
        self.wait(0.1)
        self.next_slide()
        self.play(
            AnimationGroup(
                *[
                    ApplyPointwiseFunction(
                        lambda point: point+np.random.rand(3)*0.004, datum
                    )
                    for datum in data_points
                    
                ]
            ),
        )
        self.wait(0.1)
        self.next_slide()
        self.play(
            AnimationGroup(
                Restore(data_points),
            )
        )
        self.wait(0.1)
        self.next_slide()
        self.play(self.camera.frame.animate.shift(2*RIGHT))
        self.wait(0.1)
        self.next_slide()
        compressed_data = Triangle(
                stroke_width=8.0,
                color = BLACK,
            ).to_edge(RIGHT
            ).set(height = data_points[0].get_height())
        self.play(Write(compressed_data))
        self.wait(0.1)
        self.next_slide()
        preprocessed_data = [
            Triangle().set(color = datum.get_color(), height = datum.get_height()
            ).move_to(datum.get_center())
            for datum in data_points
        ]
        self.play(
            AnimationGroup(
                *[
                    Transform(data_points[i], preprocessed_data[i])
                    for i in range(len(data_points))
                ]
            ),
        )
        self.wait(0.1)
        self.next_slide()
        
        self.play(
            AnimationGroup(
                *[
                    datum.animate.move_to(compressed_data.get_center())
                    for datum in data_points
                ],
                lag_ratio = 0.05
            )
        )
        self.wait(0.1)
        self.next_slide()
        self.play(
            Restore(data_points)
        )
        self.wait(0.1)
        self.next_slide()
        self.play(
            FadeOut(data_points, compressed_data)
        )
        self.wait(0.1)
        self.next_slide()

def related_work(self):
    def fp_formula_updater(mobj):
        mobj.become(
            MathTex(
                f"{getBitsForFloat16(x_var_tr[mobj.index].get_value())}"
            ).shift(
                2.5*RIGHT
            ).align_to(
                x_var_dec[mobj.index], UP
            )
        )
        mobj[0][0].set(color = BLUE_D)
        mobj[0][1:6].set(color = RED)
        mobj[0][6:].set(color = GREEN)
        #mobj.move_to(fp_formula_forx_exp2.get_center())
    def int_formula_updater(mobj):
        s = bin(int((x_var_tr[mobj.index].get_value())))[2:]
        s = s.rjust(16, "0")
        mobj.become(
            MathTex(
                f"{s}"
            ).shift(
                2*RIGHT
            ).align_to(
                x_var_dec[mobj.index], UP
            )
        )
        mobj[0].set(color = PURPLE)
    x_values = [1.21, 3.54, 66.73, 5.13, 12.12, 9.89]
    x_var_tr = [ValueTracker(i) for i in x_values]
    x_var_dec = []
    x_var_bin = []
    for i in range(len(x_values)):
        mobj_dec = DecimalNumber(
            x_var_tr[i].get_value(),
            num_decimal_places=10,
        )
        mobj_dec.index = i
        mobj_dec.add_updater(lambda mobj: mobj.set_value(x_var_tr[mobj.index].get_value()), call_updater=True)
        mobj_dec.set(color = BLACK)
        
        x_var_dec.append(mobj_dec)

        mobj_bin = MathTex("null")
        mobj_bin.index = i
        x_var_bin.append(mobj_bin)
    
    for i in range(len(x_values)):
        x_var_bin[i].add_updater(
            update_function = fp_formula_updater,
            call_updater = True
        )
    
    self.play(
        FadeIn(VGroup(*x_var_dec).arrange(DOWN, aligned_edge=LEFT).shift(2.5*LEFT))
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        Write(VGroup(*x_var_bin).arrange(DOWN, aligned_edge=LEFT).shift(2.5*RIGHT))
    )
    self.wait(0.1)
    self.next_slide()

    ###############
    ## If they were all the same, easy to compress, right?
    self.play(
        AnimationGroup(
            *[
                tr.animate.set_value(3.456)
                for tr in x_var_tr
            ]
        ),# rate_func=rate_functions.ease_in_out_sine)
        #run_time=5
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            *[
                x_var_tr[i].animate.set_value(x_values[i])
                for i in range(len(x_var_tr))
            ]
        ),# rate_func=rate_functions.ease_in_out_sine)
        #run_time=3
    )
    self.wait(0.1)
    self.next_slide()

    #############
    ##Change the number of decimals
    method_title = Text("Change the number of decimals", slant=ITALIC).next_to(self.title_of_the_paper, DOWN).scale(0.5)
    self.play(
        Write(method_title)
    )
    self.wait(0.1)
    self.next_slide()
    new_x_var_dec = []
    for i in range(len(x_values)):
        new_mobj_dec = DecimalNumber(
            round(x_var_tr[i].get_value(), 3),
            num_decimal_places=2,
        ).move_to(
            x_var_dec[i].get_center()
        )
        new_mobj_dec.index = i
        x_var_dec[i].clear_updaters()
        new_mobj_dec.add_updater(lambda mobj: mobj.set_value(x_var_tr[mobj.index].get_value()), call_updater=True)
        new_mobj_dec.set(color = BLACK)

        new_x_var_dec.append(new_mobj_dec)
    
    # self.play(
    #     AnimationGroup(
    #         *[
    #             Transform(
    #                 x_var_dec[i],
    #                 new_x_var_dec[i],
    #                 replace_mobject_with_target_in_scene = True
    #             )
    #             for i in range(len(x_var_dec))
    #         ]
    #     )
    # )
    self.play(
        AnimationGroup(
            *[
                FadeOut(
                    x_var_dec[i]
                )
                for i in range(len(x_values))
            ]
        )
    )
    self.play(
        AnimationGroup(
            *[
                FadeIn(
                    new_x_var_dec[i]
                )
                for i in range(len(x_values))
            ]
        )
    )
    self.wait(0.1)
    self.next_slide()

    ##Multiply by a power of 10 to remove decimals, but keep float
    self.play(
        Transform(
            method_title,
            Text("Remove decimals with *100 multiplication", slant=ITALIC).next_to(self.title_of_the_paper, DOWN).scale(0.5)
        )
    )
    self.wait(0.1)
    self.next_slide()

    self.play(
        AnimationGroup(
            *[
                tr.animate.set_value(tr.get_value()*100)
                for tr in x_var_tr
            ]
        ),# rate_func=rate_functions.ease_in_out_sine)
        #run_time=5
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            *[
                x_var_tr[i].animate.set_value(x_values[i])
                for i in range(len(x_var_tr))
            ]
        ),# rate_func=rate_functions.ease_in_out_sine)
        #run_time=3
    )
    self.wait(0.1)
    self.next_slide()

    

    #Addition method, but lossy
    self.play(
        Transform(
            method_title,
            Text("Addition method (+A)", slant=ITALIC).next_to(self.title_of_the_paper, DOWN).scale(0.5)
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            *[
                tr.animate.set_value(tr.get_value()+1800)
                for tr in x_var_tr
            ]
        ),# rate_func=rate_functions.ease_in_out_sine)
        #run_time=5
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            *[
                x_var_tr[i].animate.set_value(x_values[i])
                for i in range(len(x_var_tr))
            ]
        ),# rate_func=rate_functions.ease_in_out_sine)
        #run_time=3
    )
    self.wait(0.1)
    self.next_slide()
    
    # #Convert to int
    self.play(
        Transform(
            method_title,
            Text("Remove decimals and cast to integer", slant=ITALIC).next_to(self.title_of_the_paper, DOWN).scale(0.5)
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            *[
                tr.animate.set_value(tr.get_value()*100)
                for tr in x_var_tr
            ]
        ),# rate_func=rate_functions.ease_in_out_sine)
        #run_time=5
    )
    self.wait(0.1)
    self.next_slide()
    x_var_bin_int = []
    for i in range(len(x_values)):
        mobj_dec = MathTex("null").move_to(x_var_bin[i], aligned_edge=LEFT)
        mobj_dec.index = i
        mobj_dec.add_updater(int_formula_updater, call_updater=True)
        mobj_dec.set(color = PURPLE)
        
        x_var_bin_int.append(mobj_dec)
    
    new_x_var_int = []
    for i in range(len(x_values)):
        mobj = Integer(
            x_var_tr[i].get_value(),
            color = BLACK,
        )
        mobj.index = i
        
        mobj.move_to(
            new_x_var_dec[i].get_center()
        ).add_updater(
            lambda mobj: mobj.set_value(int(round(x_var_tr[mobj.index].get_value(), 0))), call_updater=True
        )
        new_x_var_int.append(mobj)
    self.play(
        AnimationGroup(
            *[
                FadeOut(
                    new_x_var_dec[i],
                )
                for i in range(len(x_values))
            ],
            *[
                Write(
                    new_x_var_int[i],   
                )
                for i in range(len(x_values))
            ],
            
            *[
                TransformMatchingTex(
                    x_var_bin[i],
                    x_var_bin_int[i]
                )
                for i in range(len(x_values))
            ]
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        *[FadeOut(mob) for mob in self.mobjects if mob != self.title_of_the_paper]
        # All mobjects in the screen are saved in self.mobjects
    )
    self.wait(0.1)
    self.next_slide()

def compact_bins(self):
    def set_start_end_arrow(mobj):
        mobj.put_start_and_end_on(
                self.real_line.n2p(mobj.start_number - 0.1) + mobj.vertical_shift,
                self.real_line.n2p(mobj.start_number + mobj.shift_increment.get_value()) + mobj.vertical_shift,
            )
    method_title = Text("Compact bins", slant=ITALIC).next_to(self.title_of_the_paper, DOWN).scale(0.5)
    self.play(
        Write(method_title)
    )
    self.real_line = NumberLine(
        x_range=[2**2-1, 2**3+1, 1],
        length=0.9*config.frame_width,
        color=WHITE,
        include_numbers=False,
        label_direction=UP,
        include_tip=True,
        stroke_color = BLACK
        #numbers_to_include = x_values,
        #decimal_number_config = {"num_decimal_places": 0},
    ).next_to(method_title, DOWN, buff = 1)
    labels_line = [
        MathTex(r"2^2").move_to(self.real_line.n2p(2**2) + UP*0.5),
        MathTex(r"2^3").move_to(self.real_line.n2p(2**3) + UP*0.5),
    ]
    self.play(
        Write(self.real_line)
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            *[
                Write(label)
                for label in labels_line
            ]
        )
    )
    # Write the dots
    x_values = [4.92, 5.15, 5.6, 5.83,7.13, 7.3 ]
    A_1 = 0.3
    A_2 = 1.13
    A_3 = 0.68
    dots_original = [
        Dot(
            self.real_line.n2p(x),
            color = BLACK,
            stroke_width=4,
            stroke_color = BLACK,
        ).scale(2)
        for x in x_values
    ]
    for i in range(len(dots_original)):
         dots_original[i].start_number = x_values[i]
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            *[
                Create(dot) for dot in dots_original
            ],
            lag_ratio=0.1,        
        )
    )
    self.wait(0.1)
    self.next_slide()
    
    mbit_boundaries= [
        DashedLine(self.real_line.n2p(i), self.real_line.n2p(i) + 3*DOWN, color = GREY)
        for i in [4, 5, 6, 7, 8]
    ]
    

    mantissa_annotations = [
        MathTex(r"m_1 = 0, m_2 = 0").scale(0.5).move_to(self.real_line.n2p(4.5)  + 3*DOWN),
        MathTex(r"m_1 = 0, m_2 = 1").scale(0.5).move_to(self.real_line.n2p(5.5)  + 3*DOWN),
        MathTex(r"m_1 = 1, m_2 = 0").scale(0.5).move_to(self.real_line.n2p(6.5)  + 3*DOWN),
        MathTex(r"m_1 = 1, m_2 = 1").scale(0.5).move_to(self.real_line.n2p(7.5)  + 3*DOWN),
    ]
    self.play(
         AnimationGroup(*[
                Write(line) for line in mbit_boundaries
         ]
         ),
         AnimationGroup(*[
                Write(annotation) for annotation in mantissa_annotations
         ]
         )

    )
    self.wait(0.1)
    self.next_slide()
    original_dataset_extension = DoubleArrow(
        self.real_line.n2p(x_values[0]),
        self.real_line.n2p(x_values[-1]),
        buff=0,
        color = BLACK,
        max_stroke_width_to_length_ratio=0.5,
        max_tip_length_to_length_ratio = 0.06,
    ).shift(DOWN*2.5)

    self.play(Write(original_dataset_extension))
    self.wait(0.1)
    self.next_slide()
    #Variables for shifts
    first_shift_line = Line(
        color = ORANGE,
        stroke_width=5,
    )
    first_shift_line.shift_increment = ValueTracker(0.0)
    second_shift_line = Line(
        color = BLUE,
        stroke_width=5,
    )
    second_shift_line.shift_increment = ValueTracker(0.0)
    third_shift_line = Line(
        color = PURPLE,
        stroke_width=5,
    )
    third_shift_line.shift_increment = ValueTracker(0.0)
    for dot in dots_original[4:]:
        dot.add_updater(
        lambda mobj: mobj.move_to(
            self.real_line.n2p(
                mobj.start_number 
                +
                third_shift_line.shift_increment.get_value()
            )
        ),
    )
    for dot in dots_original[2:4]:
        dot.add_updater(
        lambda mobj: mobj.move_to(
            self.real_line.n2p(
                mobj.start_number 
                +
                second_shift_line.shift_increment.get_value()
                +
                third_shift_line.shift_increment.get_value()
            )
        ),
    )
    for dot in dots_original[0:2]:
        dot.add_updater(
        lambda mobj: mobj.move_to(
            self.real_line.n2p(
                mobj.start_number 
                +
                first_shift_line.shift_increment.get_value()
                +
                second_shift_line.shift_increment.get_value()
                +
                third_shift_line.shift_increment.get_value()
            )
        ),
    )
    #First shift
    self.play(
        AnimationGroup(*[
            dot.animate.set_fill(ORANGE) for dot in dots_original[:2]
        ])
    )
    self.wait(0.1)
    self.next_slide()
    first_shift_line.start_number = x_values[0] 
    first_shift_line.vertical_shift = DOWN
    first_shift_line.add_updater(
        set_start_end_arrow,
        call_updater = True
    )
    first_shift_tip = Triangle(
        color = ORANGE,
        fill_color = ORANGE,
        fill_opacity=1,
    ).rotate(-90*DEGREES).scale(0.2).add_updater(
        lambda mobj: mobj.move_to(
            self.real_line.n2p(
                first_shift_line.start_number + first_shift_line.shift_increment.get_value()) + first_shift_line.vertical_shift
            ),
    )
    def first_label_position(mobj):
        mobj.set_value(first_shift_line.shift_increment.get_value())
        mobj.next_to(first_shift_line, DOWN, buff = 0.2)

    first_shift_label = DecimalNumber(
        color = ORANGE,
    ).scale(0.5)
    first_shift_label.add_updater(first_label_position)
    self.play(FadeIn(first_shift_line), FadeIn(first_shift_tip), FadeIn(first_shift_label))
    self.wait(0.1)
    self.next_slide()

    self.play(
        first_shift_line.shift_increment.animate.set_value(A_1)
    )
    self.wait(0.1)
    self.next_slide()

    #Second shift
    self.play(
        AnimationGroup(*[
            dot.animate.set_fill(BLUE) for dot in dots_original[2:4]
        ])
    )
    self.wait(0.1)
    self.next_slide()

    second_shift_line.start_number = x_values[2] 
    second_shift_line.vertical_shift = DOWN
    second_shift_line.add_updater(
        set_start_end_arrow,
        call_updater = True
    )
    second_shift_tip = Triangle(
        color = BLUE,
        fill_color = BLUE,
        fill_opacity=1,
    ).rotate(-90*DEGREES).scale(0.2).add_updater(
        lambda mobj: mobj.move_to(
            self.real_line.n2p(
                second_shift_line.start_number + second_shift_line.shift_increment.get_value()) + second_shift_line.vertical_shift
            ),
    )
    def second_label_position(mobj):
        mobj.set_value(second_shift_line.shift_increment.get_value())
        mobj.next_to(second_shift_line, DOWN, buff = 0.2)

    
    second_shift_label = DecimalNumber(
        color = BLUE,
    ).scale(0.5)
    second_shift_label.add_updater(second_label_position)
    self.play(FadeIn(second_shift_line), FadeIn(second_shift_tip), FadeIn(second_shift_label))
    self.wait(0.1)
    self.next_slide()
    
    self.play(
        second_shift_line.shift_increment.animate.set_value(A_2)
    )
    self.wait(0.1)
    self.next_slide()

    #Third shift
    self.play(
        AnimationGroup(*[
            dot.animate.set_fill(PURPLE) for dot in dots_original[4:]
        ])
    )
    self.wait(0.1)
    self.next_slide()

    third_shift_line.start_number = x_values[4] 
    third_shift_line.vertical_shift = DOWN
    third_shift_line.add_updater(
        set_start_end_arrow,
        call_updater = True
    )
    third_shift_tip = Triangle(
        color = PURPLE,
        fill_color = PURPLE,
        fill_opacity=1,
    ).rotate(-90*DEGREES).scale(0.2).add_updater(
        lambda mobj: mobj.move_to(
            self.real_line.n2p(
                third_shift_line.start_number + third_shift_line.shift_increment.get_value()) + third_shift_line.vertical_shift
            ),
    )
    def third_label_position(mobj):
        mobj.set_value(third_shift_line.shift_increment.get_value())
        mobj.next_to(third_shift_line, DOWN, buff = 0.2)

    
    third_shift_label = DecimalNumber(
        color = PURPLE,
    ).scale(0.5)
    third_shift_label.add_updater(third_label_position)
    self.play(FadeIn(third_shift_line), FadeIn(third_shift_tip), FadeIn(third_shift_label))
    self.wait(0.1)
    self.next_slide()
    
    self.play(
        third_shift_line.shift_increment.animate.set_value(A_3)
    )
    self.wait(0.1)
    self.next_slide()
    new_dataset_extension = DoubleArrow(
        self.real_line.n2p(7),
        self.real_line.n2p(8),
        buff=0,
        color = RED,
        max_stroke_width_to_length_ratio=1.0,
        max_tip_length_to_length_ratio = 0.12,
    ).shift(DOWN*2.5)
    shaded_original_dataset_extension = original_dataset_extension.copy().set(color = GREY)
    self.add(shaded_original_dataset_extension)
    self.play(
        Transform(
            original_dataset_extension,
            new_dataset_extension
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        *[FadeOut(mob) for mob in self.mobjects if mob != self.title_of_the_paper]
        # All mobjects in the screen are saved in self.mobjects
    )
    self.wait(0.1)
    self.next_slide()

def multiply_and_shift(self):

    method_title = Text("Multiply and Shift", slant=ITALIC).next_to(self.title_of_the_paper, DOWN).scale(0.5)
    self.play(
        Write(method_title)
    )
    self.real_line = NumberLine(
        x_range=[-1, 68, 4],
        length=0.9*config.frame_width,
        color=BLACK,
        unit_size=0.5,
        numbers_with_elongated_ticks=[0, 8, 16, 32, 64],
        numbers_to_include=[0, 8, 16, 32, 64],
        label_direction=UP,
        include_tip=True,
        stroke_color = BLACK,
        #numbers_to_include = x_values,
        decimal_number_config = {"num_decimal_places": 0},
    ).next_to(method_title, DOWN, buff = 1)
    self.real_line.numbers.set_color(BLACK)
    self.real_line.z_index=1 #To set which object behind which.
    self.play(
        Write(self.real_line)
    )
    self.wait(0.1)
    self.next_slide()
    
    ok_areas_len = 0.3 #percentage of the exponent region.
    ok_areas_rectangles = []
    exponent_boundaries = np.array([8, 16, 32, 64])
    for exp in exponent_boundaries:
        ok_areas_rectangles.append(
            Rectangle(
                color=GREEN,
                fill_opacity=0.5,
                height=0.4,
                width=np.linalg.norm(self.real_line.n2p(exp) - self.real_line.n2p(exp/2))*ok_areas_len,
                fill_color = GREEN, 
            ).move_to(self.real_line.n2p(exp), RIGHT)
        )
    self.play(
        *[
            FadeIn(rect)
            for rect in ok_areas_rectangles
        ]
    )
    self.wait(0.1)
    self.next_slide()
    #Dashed Lines
    mbit_boundaries= [
        DashedLine(self.real_line.n2p(i), self.real_line.n2p(i) + 2*DOWN, color = GREY)
        for i in np.concatenate((exponent_boundaries, [i - (i/2)*ok_areas_len for i in exponent_boundaries]))
    ]
    self.play(
        *[
            Create(
                line
            )
            for line in mbit_boundaries
        ]
    )
    self.wait(0.1)
    self.next_slide()

    #Dataset line
    self.dataset_line = NumberLine(
        x_range=[-1, 68, 4],
        length=0.9*config.frame_width,
        color=BLACK,
        unit_size=0.5,
        include_numbers = False,
        include_ticks = False,
        include_tip = False,
        label_direction=UP,
        stroke_color = BLACK,
    ).next_to(self.real_line, 4*DOWN)

    self.play(
        Write(self.dataset_line)
    )
    self.wait(0.1)
    self.next_slide()

    #Original dataset
    original_dataset = Rectangle(
        color=BLACK,
        fill_opacity=0.5,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(9) - self.dataset_line.n2p(13)),
        fill_color = BLACK, 
    ).move_to(self.dataset_line.n2p(9), LEFT)
    dataset_1 = original_dataset.copy()
    dataset_1.set_fill(BLACK,opacity=1.0)
    dataset_1.z_index=1 
    self.play(
        FadeIn(dataset_1)
    )
    self.add(original_dataset)
    self.next_slide()

    #First Move

    self.play(
        dataset_1.animate.move_to(self.dataset_line.n2p(16), RIGHT)
    )
    transformation_formula_1 = MathTex(
        r"y" , r"=" r"x", r"\oplus", r"A_1",
        font_size = 35,
    )
    transformation_formula_1.next_to(dataset_1, DOWN, buff = 1)
    transformation_formula_1[0][0].set(color = BLUE_D)

    self.play(
        AnimationGroup(
            dataset_1.animate.set_fill(BLUE_D,opacity=1.0),
            Write(transformation_formula_1)
        )
    )
    self.wait(0.1)
    self.next_slide()

    
    #Split the dataset
    dataset_portion_purple_1 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=dataset_1.width - np.linalg.norm(self.dataset_line.n2p(16) - self.dataset_line.n2p(8))*ok_areas_len,
        fill_color = PURPLE, 
    ).move_to(self.dataset_line.n2p(16 - 8*ok_areas_len), RIGHT)
    dataset_portion_purple_1.z_index = 2
    self.play(
        FadeIn(
            dataset_portion_purple_1
        )
    )
    self.remove(dataset_1)
    dataset_portion_blue_1 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(16) - self.dataset_line.n2p(8))*ok_areas_len,
        fill_color = BLUE_D, 
    ).move_to(self.dataset_line.n2p(16), RIGHT)
    self.add(dataset_portion_blue_1)
    self.next_slide()

    #Second operation
    dataset_2 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=dataset_portion_purple_1.width *4.5,
        fill_color = BLUE_D, 
    ).move_to(self.dataset_line.n2p(32), RIGHT)
    transformation_formula_2 = MathTex(
        r"y",  r"=" , r"\left(", r"x", r"\otimes", r"2", r"\right)",  r"\oplus",  r"A_2",
        font_size = 35,
    )
    transformation_formula_2.next_to(dataset_2, DOWN, buff = 1)
    transformation_formula_2[0][0].set(color = BLUE_D)
    transformation_formula_2[3][0].set(color = PURPLE)
    
    dataset_portion_purple_1_back = dataset_portion_purple_1.copy()
    self.play(
        AnimationGroup(
            ReplacementTransform(
                dataset_portion_purple_1, dataset_2
            ),
            Write(transformation_formula_2)
        )
    )
    self.wait(0.1)
    self.next_slide()
    #Split the dataset second time
    dataset_portion_purple_2 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=dataset_2.width - np.linalg.norm(self.dataset_line.n2p(32) - self.dataset_line.n2p(16))*ok_areas_len,
        fill_color = PURPLE, 
    ).move_to(self.dataset_line.n2p(32 - 16*ok_areas_len), RIGHT)
    dataset_portion_purple_2.z_index = 3
    self.play(
        FadeIn(
            dataset_portion_purple_2
        )
    )
    self.remove(dataset_2)
    dataset_portion_blue_2 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(32) - self.dataset_line.n2p(16))*ok_areas_len,
        fill_color = BLUE_D, 
    ).move_to(self.dataset_line.n2p(32), RIGHT)
    self.add(dataset_portion_blue_2)
    self.next_slide()

    #Third operation
    dataset_3 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=dataset_portion_purple_2.width *2.5,
        fill_color = BLUE_D, 
    ).move_to(self.dataset_line.n2p(64), RIGHT)
    transformation_formula_3 = MathTex(
        r"y", r"=", r"\left(", r"x", r"\otimes", r"2", r"\right)", r"\oplus",  r"A_3",
        font_size = 35,
    )
    transformation_formula_3.next_to(dataset_3, DOWN, buff = 1).align_to(dataset_3, RIGHT)
    transformation_formula_3[0][0].set(color = BLUE_D)
    transformation_formula_3[3][0].set(color = PURPLE)
    
    dataset_portion_purple_2_back = dataset_portion_purple_2.copy()
    self.play(
        AnimationGroup(
            ReplacementTransform(
                dataset_portion_purple_2, dataset_3
            ),
            Write(transformation_formula_3)
        )
    )
    self.wait(0.1)
    self.next_slide()

    # # Remove all formulas
    # self.play(
    #     AnimationGroup(
    #         FadeOut(transformation_formula_1),
    #         FadeOut(transformation_formula_2),
    #         FadeOut(transformation_formula_3)
    #     )
    # )

    #Revert Third Operation
    transformation_formula_3_inverse = MathTex(
        r"x",  r"=" ,r"\left(", r"y", r"\ominus", r"A_3", r"\right)",r"\oslash", r"2",
        font_size = 35,
    )
    transformation_formula_3_inverse.move_to(transformation_formula_3.get_center())
    transformation_formula_3_inverse[0][0].set(color = PURPLE)
    transformation_formula_3_inverse[3][0].set(color = BLUE_D)

    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_3,transformation_formula_3_inverse),
            ReplacementTransform(dataset_3, dataset_portion_purple_2_back)
        )
    )
    self.wait(0.1)
    self.next_slide()

    self.play(
        AnimationGroup(
            FadeIn(dataset_2),
            FadeOut(dataset_portion_purple_2_back),
            FadeOut(dataset_portion_blue_2)
        )
    )
    self.wait(0.1)
    self.next_slide()

    transformation_formula_2_inverse = MathTex(
        r"x",  r"=" ,r"\left(", r"y", r"\ominus", r"A_2", r"\right)",r"\oslash", r"2",
        font_size = 35,
    )
    transformation_formula_2_inverse.move_to(transformation_formula_2.get_center())
    transformation_formula_2_inverse[0][0].set(color = PURPLE)
    transformation_formula_2_inverse[3][0].set(color = BLUE_D)

    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_2,transformation_formula_2_inverse),
            ReplacementTransform(dataset_2, dataset_portion_purple_1_back)
        )
    )
    self.wait(0.1)
    self.next_slide()

    self.play(
        AnimationGroup(
            FadeIn(dataset_1),
            FadeOut(dataset_portion_purple_1_back, dataset_portion_blue_1)
        )
    )
    self.wait(0.1)
    self.next_slide()
    transformation_formula_1_inverse = MathTex(
        r"x",  r"=", r"y", r"\ominus", r"A_1",
        font_size = 35,
    )
    transformation_formula_1_inverse.move_to(transformation_formula_1.get_center())
    transformation_formula_1_inverse[2][0].set(color = BLUE_D)
    self.play(
        AnimationGroup(
            ReplacementTransform(dataset_1, original_dataset),
            TransformMatchingTex(transformation_formula_1,transformation_formula_1_inverse),
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        *[FadeOut(mob) for mob in self.mobjects if mob != self.title_of_the_paper]
        # All mobjects in the screen are saved in self.mobjects
    )
    self.wait(0.1)
    self.next_slide()

def shift_and_separate_even_from_odd(self):
    method_title = Text("Shift and Separate Even from Odd", slant=ITALIC).next_to(self.title_of_the_paper, DOWN).scale(0.5)
    self.play(
        Write(method_title)
    )
    self.real_line = NumberLine(
        x_range=[-1, 68, 4],
        length=0.9*config.frame_width,
        color=BLACK,
        unit_size=0.5,
        numbers_with_elongated_ticks=[0, 8, 16, 32, 64],
        numbers_to_include=[0, 8, 16, 32, 64],
        label_direction=UP,
        include_tip=True,
        stroke_color = BLACK,
        #numbers_to_include = x_values,
        decimal_number_config = {"num_decimal_places": 0},
    ).next_to(method_title, DOWN, buff = 1)
    self.real_line.numbers.set_color(BLACK)
    self.real_line.z_index=1 #To set which object behind which.
    self.play(
        Write(self.real_line)
    )
    self.wait(0.1)
    self.next_slide()
    
    ok_areas_len = 0.3 #percentage of the exponent region.
    ok_areas_rectangles = []
    exponent_boundaries = np.array([8, 16, 32, 64])
    for exp in exponent_boundaries:
        ok_areas_rectangles.append(
            Rectangle(
                color=GREEN,
                fill_opacity=0.5,
                height=0.4,
                width=np.linalg.norm(self.real_line.n2p(exp) - self.real_line.n2p(exp/2))*ok_areas_len,
                fill_color = GREEN, 
            ).move_to(self.real_line.n2p(exp), RIGHT)
        )
    self.play(
        *[
            FadeIn(rect)
            for rect in ok_areas_rectangles
        ]
    )
    self.wait(0.1)
    self.next_slide()
    #Dashed Lines
    mbit_boundaries= [
        DashedLine(self.real_line.n2p(i), self.real_line.n2p(i) + 2*DOWN, color = GREY)
        for i in np.concatenate((exponent_boundaries, [i - (i/2)*ok_areas_len for i in exponent_boundaries]))
    ]
    self.play(
        *[
            Create(
                line
            )
            for line in mbit_boundaries
        ]
    )
    self.wait(0.1)
    self.next_slide()

    #Dataset line
    self.dataset_line = NumberLine(
        x_range=[-1, 68, 4],
        length=0.9*config.frame_width,
        color=BLACK,
        unit_size=0.5,
        include_numbers = False,
        include_ticks = False,
        include_tip = False,
        label_direction=UP,
        stroke_color = BLACK,
    ).next_to(self.real_line, 4*DOWN)

    self.play(
        Write(self.dataset_line)
    )
    self.wait(0.1)
    self.next_slide()

    #Original dataset
    original_dataset = Rectangle(
        color=BLACK,
        fill_opacity=0.5,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(9) - self.dataset_line.n2p(13)),
        fill_color = BLACK, 
    ).move_to(self.dataset_line.n2p(9), LEFT)
    dataset_1 = original_dataset.copy()
    dataset_1.set_fill(BLACK,opacity=1.0)
    dataset_1.z_index=1 
    self.play(
        FadeIn(dataset_1)
    )
    self.add(original_dataset)
    self.next_slide()

    #First Move

    self.play(
        dataset_1.animate.move_to(self.dataset_line.n2p(16), RIGHT)
    )
    transformation_formula_1 = MathTex(
        r"y" , r"=", r"x", r"\oplus", r"A_{\mathrm{align}}",
        font_size = 35,
    )
    transformation_formula_1.next_to(dataset_1, DOWN, buff = 0.25)
    transformation_formula_1[0][0].set(color = GREY)

    self.play(
        AnimationGroup(
            dataset_1.animate.set_fill(GREY,opacity=1.0),
            Write(transformation_formula_1)
        )
    )
    self.wait(0.1)
    self.next_slide()

    
    #Split the dataset
    dataset_portion_purple_1 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=dataset_1.width - np.linalg.norm(self.dataset_line.n2p(16) - self.dataset_line.n2p(8))*ok_areas_len,
        fill_color = PURPLE, 
    ).move_to(self.dataset_line.n2p(16 - 8*ok_areas_len), RIGHT)
    dataset_portion_purple_1.z_index = 2
    self.play(
        FadeIn(
            dataset_portion_purple_1
        )
    )
    self.remove(dataset_1)
    dataset_portion_grey_1 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(16) - self.dataset_line.n2p(8))*ok_areas_len,
        fill_color = GREY, 
    ).move_to(self.dataset_line.n2p(16), RIGHT)
    self.add(dataset_portion_grey_1)
    self.next_slide()

    #Second operation
    #EVEN
    dataset_portion_purple_1_back = dataset_portion_purple_1.copy()
    dataset_2_even = Rectangle(
        color = BLACK,
        fill_opacity = 1.0,
        height = 0.3,
        width = np.linalg.norm(self.dataset_line.n2p(32) - self.dataset_line.n2p(29)),
        fill_color = BLUE_D,
    ).move_to(self.dataset_line.n2p(32), RIGHT)
    transformation_formula_2_even = MathTex(
        r"y",  r"=" , r"x^{\mathrm{even}}", r"\oplus",  r"A_1^{\mathrm{even}}",
        font_size = 35,
    )
    transformation_formula_2_even.next_to(dataset_2_even, UP, buff = 0.25)
    transformation_formula_2_even[0][0].set(color = BLUE_D)
    transformation_formula_2_even[2].set(color = PURPLE)

    self.play(
        AnimationGroup(
            TransformFromCopy(
                dataset_portion_purple_1, dataset_2_even
            ),
            Write(transformation_formula_2_even)
        )
    )
    self.wait(0.1)
    self.next_slide()
    #ODD
    dataset_2_odd = Rectangle(
        color = BLACK,
        fill_opacity = 1.0,
        height = 0.3,
        width = np.linalg.norm(self.dataset_line.n2p(29) - self.dataset_line.n2p(25)),
        fill_color = ORANGE,
    ).move_to(self.dataset_line.n2p(29), RIGHT)
    transformation_formula_2_odd = MathTex(
        r"y",  r"=" , r"x^{\mathrm{odd}}", r"\oplus",  r"A_1^{\mathrm{odd}}",
        font_size = 35,
    )
    transformation_formula_2_odd.next_to(dataset_2_even, DOWN, buff = 0.25) #kept even for alignment
    transformation_formula_2_odd[0][0].set(color = ORANGE)
    transformation_formula_2_odd[2].set(color = PURPLE)

    self.play(
        AnimationGroup(
            ReplacementTransform(
                dataset_portion_purple_1, dataset_2_odd
            ),
            Write(transformation_formula_2_odd)
        )
    )
    self.wait(0.1)
    self.next_slide()

    #Split the dataset second time
    dataset_portion_purple_2 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(32-(32-16)*ok_areas_len) - self.dataset_line.n2p(25)),
        fill_color = PURPLE, 
    ).move_to(self.dataset_line.n2p(32 - 16*ok_areas_len), RIGHT)
    dataset_portion_purple_2.z_index = 3
    self.play(
        FadeIn(
            dataset_portion_purple_2
        )
    )
    self.remove(dataset_2_odd)
    dataset_portion_odd_keep_2 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=np.linalg.norm(dataset_2_even.get_left() - self.dataset_line.n2p(32-(32-16)*ok_areas_len)),
        fill_color = ORANGE, 
    ).move_to(self.dataset_line.n2p(32-(32-16)*ok_areas_len), LEFT)
    self.add(dataset_portion_odd_keep_2)
    self.next_slide()

    #Third operation
    #EVEN
    dataset_portion_purple_2_back = dataset_portion_purple_2.copy()
    dataset_3_even = Rectangle(
        color = BLACK,
        fill_opacity = 1.0,
        height = 0.3,
        width = np.linalg.norm(self.dataset_line.n2p(64) - self.dataset_line.n2p(59)),
        fill_color = BLUE_D,
    ).move_to(self.dataset_line.n2p(64), RIGHT)
    transformation_formula_3_even = MathTex(
        r"y",  r"=" , r"x^{\mathrm{even}}", r"\oplus",  r"A_2^{\mathrm{even}}",
        font_size = 35,
    )
    transformation_formula_3_even.next_to(dataset_3_even, UP, buff = 0.25)
    transformation_formula_3_even[0][0].set(color = BLUE_D)
    transformation_formula_3_even[2].set(color = PURPLE)
    
    dataset_portion_purple_2.z_index = 4
    dataset_3_even.z_index = 4
    self.play(
        AnimationGroup(
            TransformFromCopy(
                dataset_portion_purple_2, dataset_3_even
            ),
            Write(transformation_formula_3_even)
        )
    )
    self.wait(0.1)
    self.next_slide()
    #ODD
    dataset_3_odd = Rectangle(
        color = BLACK,
        fill_opacity = 1.0,
        height = 0.3,
        width = np.linalg.norm(self.dataset_line.n2p(59) - self.dataset_line.n2p(56)),
        fill_color = ORANGE,
    ).move_to(self.dataset_line.n2p(59), RIGHT)
    transformation_formula_3_odd = MathTex(
        r"y",  r"=" , r"x^{\mathrm{odd}}", r"\oplus",  r"A_2^{\mathrm{odd}}",
        font_size = 35,
    )
    transformation_formula_3_odd.next_to(dataset_3_even, DOWN, buff = 0.25) #kept even for alignment
    transformation_formula_3_odd[0][0].set(color = ORANGE)
    transformation_formula_3_odd[2].set(color = PURPLE)

    self.play(
        AnimationGroup(
            ReplacementTransform(
                dataset_portion_purple_2, dataset_3_odd
            ),
            Write(transformation_formula_3_odd)
        )
    )
    self.wait(0.1)
    self.next_slide()
    
    ## Revert from 64 region
    transformation_formula_3_even_inverse = MathTex(
        r"x^{\mathrm{even}}",r"=",  r"y",  r"\ominus",  r"A_2^{\mathrm{even}}",
        font_size = 35,
    )
    transformation_formula_3_even_inverse.move_to(transformation_formula_3_even.get_center())
    transformation_formula_3_even_inverse[0].set(color = PURPLE)
    transformation_formula_3_even_inverse[2].set(color = BLUE_D)
    dataset_portion_purple_2_back.z_index = 4
    dataset_3_even.z_index = 4
    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_3_even,transformation_formula_3_even_inverse),
            ReplacementTransform(dataset_3_even, dataset_portion_purple_2_back)
        )
    )
    self.wait(0.1)
    self.next_slide()

    transformation_formula_3_odd_inverse = MathTex(
        r"x^{\mathrm{odd}}",r"=",  r"y",  r"\ominus",  r"A_2^{\mathrm{odd}}",
        font_size = 35,
    )
    transformation_formula_3_odd_inverse.move_to(transformation_formula_3_odd.get_center())
    transformation_formula_3_odd_inverse[0].set(color = PURPLE)
    transformation_formula_3_odd_inverse[2].set(color = ORANGE)
    dataset_portion_purple_2_back.z_index = 4
    dataset_3_odd.z_index = 4
    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_3_odd,transformation_formula_3_odd_inverse),
            ReplacementTransform(dataset_3_odd, dataset_portion_purple_2_back)
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            FadeIn(dataset_2_odd),
            FadeOut(dataset_portion_purple_2_back),
            FadeOut(dataset_portion_odd_keep_2)
        )
    )
    self.wait(0.1)
    self.next_slide()

    ## Revert from 32 region
    transformation_formula_2_even_inverse = MathTex(
        r"x^{\mathrm{even}}",r"=",  r"y",  r"\ominus",  r"A_1^{\mathrm{even}}",
        font_size = 35,
    )
    transformation_formula_2_even_inverse.move_to(transformation_formula_2_even.get_center())
    transformation_formula_2_even_inverse[0].set(color = PURPLE)
    transformation_formula_2_even_inverse[2].set(color = BLUE_D)
    dataset_portion_purple_2_back.z_index = 4
    dataset_2_even.z_index = 4
    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_2_even,transformation_formula_2_even_inverse),
            ReplacementTransform(dataset_2_even, dataset_portion_purple_1_back)
        )
    )
    self.wait(0.1)
    self.next_slide()

    transformation_formula_2_odd_inverse = MathTex(
        r"x^{\mathrm{odd}}",r"=",  r"y",  r"\ominus",  r"A_2^{\mathrm{odd}}",
        font_size = 35,
    )
    transformation_formula_2_odd_inverse.move_to(transformation_formula_2_odd.get_center())
    transformation_formula_2_odd_inverse[0].set(color = PURPLE)
    transformation_formula_2_odd_inverse[2].set(color = ORANGE)
    dataset_portion_purple_2_back.z_index = 4
    dataset_2_odd.z_index = 4
    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_2_odd,transformation_formula_2_odd_inverse),
            ReplacementTransform(dataset_2_odd, dataset_portion_purple_1_back)
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            FadeIn(dataset_1),
            FadeOut(dataset_portion_purple_1_back),
            FadeOut(dataset_portion_grey_1)
        )
    )
    self.wait(0.1)
    self.next_slide()

    #Reverse from 16 region
    transformation_formula_1_inverse = MathTex(
        r"x",r"=",  r"y",  r"\ominus",  r"A_{\mathrm{align}}",
        font_size = 35,
    )
    transformation_formula_1_inverse.move_to(transformation_formula_1.get_center())
    transformation_formula_1_inverse[2].set(color = GREY)
    self.play(
        AnimationGroup(
            ReplacementTransform(
                dataset_1, original_dataset
            ),
            TransformMatchingTex(transformation_formula_1, transformation_formula_1_inverse)
        )
       
    )
    self.wait(0.1)
    self.next_slide()

    self.play(
        *[FadeOut(mob) for mob in self.mobjects if mob != self.title_of_the_paper]
        # All mobjects in the screen are saved in self.mobjects
    )
    self.wait(0.1)
    self.next_slide()

def shift_and_save_evenness(self):
    method_title = Text("Shift and Save Evenness", slant=ITALIC).next_to(self.title_of_the_paper, DOWN).scale(0.5)
    self.play(
        Write(method_title)
    )
    self.real_line = NumberLine(
        x_range=[-1, 68, 4],
        length=0.9*config.frame_width,
        color=BLACK,
        unit_size=0.5,
        numbers_with_elongated_ticks=[0, 8, 16, 32, 64],
        numbers_to_include=[0, 8, 16, 32, 64],
        label_direction=UP,
        include_tip=True,
        stroke_color = BLACK,
        #numbers_to_include = x_values,
        decimal_number_config = {"num_decimal_places": 0},
    ).next_to(method_title, DOWN, buff = 1)
    self.real_line.numbers.set_color(BLACK)
    self.real_line.z_index=1 #To set which object behind which.
    self.play(
        Write(self.real_line)
    )
    self.wait(0.1)
    self.next_slide()
    
    ok_areas_len = 0.3 #percentage of the exponent region.
    ok_areas_rectangles = []
    exponent_boundaries = np.array([8, 16, 32, 64])
    for exp in exponent_boundaries:
        ok_areas_rectangles.append(
            Rectangle(
                color=GREEN,
                fill_opacity=0.5,
                height=0.4,
                width=np.linalg.norm(self.real_line.n2p(exp) - self.real_line.n2p(exp/2))*ok_areas_len,
                fill_color = GREEN, 
            ).move_to(self.real_line.n2p(exp), RIGHT)
        )
    self.play(
        *[
            FadeIn(rect)
            for rect in ok_areas_rectangles
        ]
    )
    self.wait(0.1)
    self.next_slide()
    #Dashed Lines
    mbit_boundaries= [
        DashedLine(self.real_line.n2p(i), self.real_line.n2p(i) + 2*DOWN, color = GREY)
        for i in np.concatenate((exponent_boundaries, [i - (i/2)*ok_areas_len for i in exponent_boundaries]))
    ]
    self.play(
        *[
            Create(
                line
            )
            for line in mbit_boundaries
        ]
    )
    self.wait(0.1)
    self.next_slide()

    #Dataset line
    self.dataset_line = NumberLine(
        x_range=[-1, 68, 4],
        length=0.9*config.frame_width,
        color=BLACK,
        unit_size=0.5,
        include_numbers = False,
        include_ticks = False,
        include_tip = False,
        label_direction=UP,
        stroke_color = BLACK,
    ).next_to(self.real_line, 4*DOWN)

    self.play(
        Write(self.dataset_line)
    )
    self.wait(0.1)
    self.next_slide()

    #Original dataset
    original_dataset = Rectangle(
        color=BLACK,
        fill_opacity=0.5,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(9) - self.dataset_line.n2p(13)),
        fill_color = BLACK, 
    ).move_to(self.dataset_line.n2p(9), LEFT)
    dataset_1 = original_dataset.copy()
    dataset_1.set_fill(BLACK,opacity=1.0)
    dataset_1.z_index=1 
    self.play(
        FadeIn(dataset_1)
    )
    self.add(original_dataset)
    self.next_slide()

    #First Move

    self.play(
        dataset_1.animate.move_to(self.dataset_line.n2p(16), RIGHT)
    )
    transformation_formula_1 = MathTex(
        r"y" , r"=", r"x", r"\oplus", r"A_{\mathrm{align}}",
        font_size = 35,
    )
    transformation_formula_1.next_to(dataset_1, DOWN, buff = 0.25)
    transformation_formula_1[0][0].set(color = GREY)

    self.play(
        AnimationGroup(
            dataset_1.animate.set_fill(GREY,opacity=1.0),
            Write(transformation_formula_1)
        )
    )
    self.wait(0.1)
    self.next_slide()

    
    #Split the dataset
    dataset_portion_purple_1 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=dataset_1.width - np.linalg.norm(self.dataset_line.n2p(16) - self.dataset_line.n2p(8))*ok_areas_len,
        fill_color = PURPLE, 
    ).move_to(self.dataset_line.n2p(16 - 8*ok_areas_len), RIGHT)
    dataset_portion_purple_1.z_index = 2
    self.play(
        FadeIn(
            dataset_portion_purple_1
        )
    )
    self.remove(dataset_1)
    dataset_portion_grey_1 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(16) - self.dataset_line.n2p(8))*ok_areas_len,
        fill_color = GREY, 
    ).move_to(self.dataset_line.n2p(16), RIGHT)
    self.add(dataset_portion_grey_1)
    self.next_slide()

    #Second operation
    #EVEN
    dataset_portion_purple_1_back = dataset_portion_purple_1.copy()
    dataset_2 = Rectangle(
        color = BLACK,
        fill_opacity = 1.0,
        height = 0.3,
        width = np.linalg.norm(self.dataset_line.n2p(32) - self.dataset_line.n2p(25)),
        fill_color = BLUE_D,
    ).move_to(self.dataset_line.n2p(32), RIGHT)
    transformation_formula_2_even = MathTex(
        r"y",  r"=" , r"x^{\mathrm{even}}", r"\oplus",  r"A_1^{\mathrm{even}}",
        font_size = 35,
    )
    transformation_formula_2_even.next_to(dataset_2, UP, buff = 0.25)
    transformation_formula_2_even[0][0].set(color = BLUE_D)
    transformation_formula_2_even[2].set(color = PURPLE)

    self.play(
        AnimationGroup(
            TransformFromCopy(
                dataset_portion_purple_1, dataset_2
            ),
            Write(transformation_formula_2_even)
        )
    )
    self.wait(0.1)
    self.next_slide()
    #ODD
    transformation_formula_2_odd = MathTex(
        r"y",  r"=" , r"x^{\mathrm{odd}}", r"\oplus",  r"A_1^{\mathrm{odd}}",
        font_size = 35,
    )
    transformation_formula_2_odd.next_to(dataset_2, DOWN, buff = 0.25) #kept even for alignment
    transformation_formula_2_odd[0][0].set(color = BLUE_D)
    transformation_formula_2_odd[2].set(color = PURPLE)

    self.play(
        AnimationGroup(
            ReplacementTransform(
                dataset_portion_purple_1, dataset_2
            ),
            Write(transformation_formula_2_odd)
        )
    )
    self.wait(0.1)
    self.next_slide()

    #Split the dataset second time
    dataset_portion_purple_2 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(32-(32-16)*ok_areas_len) - self.dataset_line.n2p(25)),
        fill_color = PURPLE, 
    ).move_to(self.dataset_line.n2p(32 - 16*ok_areas_len), RIGHT)
    dataset_portion_purple_2.z_index = 3
    self.play(
        FadeIn(
            dataset_portion_purple_2
        )
    )
    self.remove(dataset_2)
    dataset_portion_keep_2 = Rectangle(
        color=BLACK,
        fill_opacity=1.0,
        height=0.3,
        width=np.linalg.norm(self.dataset_line.n2p(32) - self.dataset_line.n2p(32-(32-16)*ok_areas_len)),
        fill_color = BLUE_D, 
    ).move_to(self.dataset_line.n2p(32), RIGHT)
    self.add(dataset_portion_keep_2)
    self.next_slide()

    #Third operation
    #EVEN
    dataset_portion_purple_2_back = dataset_portion_purple_2.copy()
    dataset_3 = Rectangle(
        color = BLACK,
        fill_opacity = 1.0,
        height = 0.3,
        width = np.linalg.norm(self.dataset_line.n2p(64) - self.dataset_line.n2p(56)),
        fill_color = BLUE_D,
    ).move_to(self.dataset_line.n2p(64), RIGHT)
    transformation_formula_3_even = MathTex(
        r"y",  r"=" , r"x^{\mathrm{even}}", r"\oplus",  r"A_2^{\mathrm{even}}",
        font_size = 35,
    )
    transformation_formula_3_even.next_to(dataset_3, UP, buff = 0.25)
    transformation_formula_3_even[0][0].set(color = BLUE_D)
    transformation_formula_3_even[2].set(color = PURPLE)
    
    dataset_portion_purple_2.z_index = 4
    dataset_3.z_index = 4
    self.play(
        AnimationGroup(
            TransformFromCopy(
                dataset_portion_purple_2, dataset_3
            ),
            Write(transformation_formula_3_even)
        )
    )
    self.wait(0.1)
    self.next_slide()
    #ODD

    transformation_formula_3_odd = MathTex(
        r"y",  r"=" , r"x^{\mathrm{odd}}", r"\oplus",  r"A_2^{\mathrm{odd}}",
        font_size = 35,
    )
    transformation_formula_3_odd.next_to(dataset_3, DOWN, buff = 0.25) #kept even for alignment
    transformation_formula_3_odd[0][0].set(color = BLUE_D)
    transformation_formula_3_odd[2].set(color = PURPLE)

    self.play(
        AnimationGroup(
            ReplacementTransform(
                dataset_portion_purple_2, dataset_3
            ),
            Write(transformation_formula_3_odd)
        )
    )
    self.wait(0.1)
    self.next_slide()
    
    ## Revert from 64 region
    transformation_formula_3_even_inverse = MathTex(
        r"x^{\mathrm{even}}",r"=",  r"y",  r"\ominus",  r"A_2^{\mathrm{even}}",
        font_size = 35,
    )
    transformation_formula_3_even_inverse.move_to(transformation_formula_3_even.get_center())
    transformation_formula_3_even_inverse[0].set(color = PURPLE)
    transformation_formula_3_even_inverse[2].set(color = BLUE_D)
    dataset_portion_purple_2_back.z_index = 4
    dataset_3.z_index = 4
    dataset_3_copy = dataset_3.copy()
    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_3_even,transformation_formula_3_even_inverse),
            ReplacementTransform(dataset_3_copy, dataset_portion_purple_2_back)
        )
    )
    self.wait(0.1)
    self.next_slide()

    transformation_formula_3_odd_inverse = MathTex(
        r"x^{\mathrm{odd}}",r"=",  r"y",  r"\ominus",  r"A_2^{\mathrm{odd}}",
        font_size = 35,
    )
    transformation_formula_3_odd_inverse.move_to(transformation_formula_3_odd.get_center())
    transformation_formula_3_odd_inverse[0].set(color = PURPLE)
    transformation_formula_3_odd_inverse[2].set(color = BLUE_D)
    dataset_portion_purple_2_back.z_index = 4
    dataset_3.z_index = 4
    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_3_odd,transformation_formula_3_odd_inverse),
            ReplacementTransform(dataset_3, dataset_portion_purple_2_back)
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            FadeIn(dataset_2),
            FadeOut(dataset_portion_purple_2_back),
            FadeOut(dataset_portion_keep_2)
        )
    )
    self.wait(0.1)
    self.next_slide()

    ## Revert from 32 region
    transformation_formula_2_even_inverse = MathTex(
        r"x^{\mathrm{even}}",r"=",  r"y",  r"\ominus",  r"A_1^{\mathrm{even}}",
        font_size = 35,
    )
    transformation_formula_2_even_inverse.move_to(transformation_formula_2_even.get_center())
    transformation_formula_2_even_inverse[0].set(color = PURPLE)
    transformation_formula_2_even_inverse[2].set(color = BLUE_D)
    dataset_portion_purple_2_back.z_index = 4
    dataset_2.z_index = 4
    dataset_2_copy = dataset_2.copy()
    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_2_even,transformation_formula_2_even_inverse),
            ReplacementTransform(dataset_2_copy, dataset_portion_purple_1_back)
        )
    )
    self.wait(0.1)
    self.next_slide()

    transformation_formula_2_odd_inverse = MathTex(
        r"x^{\mathrm{odd}}",r"=",  r"y",  r"\ominus",  r"A_2^{\mathrm{odd}}",
        font_size = 35,
    )
    transformation_formula_2_odd_inverse.move_to(transformation_formula_2_odd.get_center())
    transformation_formula_2_odd_inverse[0].set(color = PURPLE)
    transformation_formula_2_odd_inverse[2].set(color = BLUE_D)
    dataset_portion_purple_2_back.z_index = 4
    dataset_2.z_index = 4
    self.play( 
        AnimationGroup(
            TransformMatchingTex(transformation_formula_2_odd,transformation_formula_2_odd_inverse),
            ReplacementTransform(dataset_2, dataset_portion_purple_1_back)
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            FadeIn(dataset_1),
            FadeOut(dataset_portion_purple_1_back),
            FadeOut(dataset_portion_grey_1)
        )
    )
    self.wait(0.1)
    self.next_slide()

    #Reverse from 16 region
    transformation_formula_1_inverse = MathTex(
        r"x",r"=",  r"y",  r"\ominus",  r"A_{\mathrm{align}}",
        font_size = 35,
    )
    transformation_formula_1_inverse.move_to(transformation_formula_1.get_center())
    transformation_formula_1_inverse[2].set(color = GREY)
    self.play(
        AnimationGroup(
            ReplacementTransform(
                dataset_1, original_dataset
            ),
            TransformMatchingTex(transformation_formula_1, transformation_formula_1_inverse)
        )
       
    )
    self.wait(0.1)
    self.next_slide()

    self.play(
        *[FadeOut(mob) for mob in self.mobjects if mob != self.title_of_the_paper]
        # All mobjects in the screen are saved in self.mobjects
    )
    self.wait(0.1)
    self.next_slide()

def show_results(self):
    colors_of_result = [
        "#E3B505",
        RED,
        BLUE,
        TEAL
    ]
    chicago_results = ImageMobject("./totalChicagoTaxiTrip1000.png")
    self.play(
        FadeIn(chicago_results)
    )
    compact_bin_best = Dot(
        self.camera.frame_center + 4.3*LEFT + 0.7*DOWN,
        radius=0.1,
        fill_opacity=1.0,
        color = BLACK,
        stroke_width=2,
    ).set_fill(colors_of_result[0])

    multiply_and_shift_best = Dot(
        self.camera.frame_center + 1.3*LEFT + 0.76*DOWN,
        radius=0.1,
        fill_opacity=1.0,
        color = BLACK,
        stroke_width=2,
    ).set_fill(colors_of_result[1])

    shift_and_separate_best = Dot(
        self.camera.frame_center + 1.6*RIGHT + 0.65*DOWN,
        radius=0.1,
        fill_opacity=1.0,
        color = BLACK,
        stroke_width=2,
    ).set_fill(colors_of_result[2])

    shift_and_save_best = Dot(
        self.camera.frame_center + 3.64*RIGHT + 0.62*DOWN,
        radius=0.1,
        fill_opacity=1.0,
        color = BLACK,
        stroke_width=2,
    ).set_fill(colors_of_result[3])

    self.play(
        Create(compact_bin_best),
        Create(multiply_and_shift_best),
        Create(shift_and_separate_best),
        Create(shift_and_save_best)
    )
    self.wait(0.1)
    self.next_slide()


    # Build the graph
    ax = Axes(
        x_range = [0, 12, 2],
        y_range = [-45, 0, 10],
        axis_config={
            "include_tip": False,
            "font_size": 24,
            "include_numbers": True,
            "color": BLACK,
            "label_direction":UP,
        },
        x_length = 0.3*self.camera.frame.width,
        y_length = 0.6*self.camera.frame.height,
    ).add_coordinates().shift(DOWN*0.5)
    ax.x_axis.numbers.set(color = BLACK)
    ax.y_axis.numbers.set(color = BLACK)
    ax.center()
    y_label = ax.get_y_axis_label(
        Tex("Compressed Dataset Size Reduction (\%)").scale(0.65).rotate(90 * DEGREES),
        edge=LEFT, direction=LEFT, buff = 0.4
    )
    x_label = ax.get_x_axis_label(
        Tex("Guaranteed shared mantissa bits").scale(0.65),
        edge=UP, direction=UP, buff=0.2
    )#.shift(3.0*LEFT)
    
    dashed_lines = VGroup()
    for x in np.arange(0.0, 14.0, 2.0):
        dashed_lines.add(
            ax.get_vertical_line(
                ax.coords_to_point(x,-45),
                line_config={
                    "dashed_ratio": 0.55,
                    "stroke_color":GREY,
                }
            )
        )
    
    for y in np.arange(-40, 0, 10):
        dashed_lines.add(
            ax.get_horizontal_line(
                ax.coords_to_point(12,y),
                line_config={
                    "dashed_ratio": 0.55,
                    "stroke_color":GREY,
                }
            )
        )
    
    #ax.set(color = BLACK)
    
    dot_config = {
        "radius" : DEFAULT_DOT_RADIUS*2.0,
        "fill_opacity":0.5,
        "stroke_width": 2.0,
        "stroke_color":BLACK,
    }
    # TaxiDB
    dot_taxi = [
        Dot(
            ax.coords_to_point(11, -37),
            fill_color = colors_of_result[0],
            **dot_config,
        ),
        Dot(
            ax.coords_to_point(5, -42),
            fill_color = colors_of_result[1],
            **dot_config,
        ),
        Dot(
            ax.coords_to_point(4, -34),
            fill_color = colors_of_result[2],
            **dot_config,
        ),
        Dot(
            ax.coords_to_point(5, -30),
            fill_color = colors_of_result[3],
            **dot_config,
        ),
    ]
    # UciDB
    triangle_uci = [
        Triangle(
            fill_color = colors_of_result[0], 
            **dot_config
        ).rotate(60*DEGREES).scale(1.2).move_to(
            ax.coords_to_point(1, -2)
        ),
        Triangle(
            fill_color = colors_of_result[1],
            **dot_config
        ).rotate(60*DEGREES).scale(1.2).move_to(
            ax.coords_to_point(2, -4)
        ),
        Triangle(
            fill_color = colors_of_result[2],
            **dot_config
        ).rotate(60*DEGREES).scale(1.2).move_to(
            ax.coords_to_point(6, -6)
        ),
        Triangle(
            fill_color = colors_of_result[3],
            **dot_config
        ).rotate(60*DEGREES).scale(1.2).move_to(
            ax.coords_to_point(5, -5)
        )
    ]
    
    ## LEGEND
    legend_shape = Tex(
        "SHAPE: Dataset",
        font_size = 30
    ).shift(2*UP)
    legend_dot = Dot(
        radius=DEFAULT_DOT_RADIUS*2.0,
        color= GREEN,
        fill_opacity=0.5,
        stroke_width= 2.0,
        stroke_color=BLACK,
        fill_color=self.camera.background_color,
    ).next_to(legend_shape, DOWN).align_to(legend_shape, LEFT)
    legend_dot_desc = Tex(
        ": Uci",
        font_size = 30
    ).next_to(legend_dot, RIGHT)
    legend_triangle = Triangle(
        radius=DEFAULT_DOT_RADIUS*2.0,
        color= GREEN,
        fill_opacity=0.5,
        stroke_width= 2.0,
        stroke_color=BLACK,
        fill_color=self.camera.background_color,
    ).rotate(60*DEGREES).scale(1.2).next_to(legend_dot, DOWN).align_to(legend_shape, LEFT)
    legend_triangle_desc = Tex(
        ": Taxi",
        font_size = 30
    ).next_to(legend_triangle, RIGHT)

    legend_color = Tex(
        "COLORS: Techniques",
        font_size = 30
    ).next_to(legend_triangle, DOWN).align_to(legend_triangle, LEFT)
    
    legend_compact_bins = Rectangle(
        color=BLACK,
        fill_opacity = 0.5,
        fill_color = colors_of_result[0],
        height=0.2, 
        width=0.4,
    ).next_to(legend_color, DOWN).align_to(legend_color, LEFT)
    legend_compact_bins_desc = Tex(
        ": Compact Bins",
        font_size = 30
    ).next_to(legend_compact_bins, RIGHT)

    legend_multiply_and_shift = Rectangle(
        color=BLACK,
        fill_opacity = 0.5,
        fill_color = colors_of_result[1],
        height=0.2, 
        width=0.4,
    ).next_to(legend_compact_bins, DOWN).align_to(legend_compact_bins, LEFT)
    legend_multiply_and_shift_desc = Tex(
        ": Multiply and Shift",
        font_size = 30
    ).next_to(legend_multiply_and_shift, RIGHT)

    legend_shift_and_separate = Rectangle(
        color=BLACK,
        fill_opacity = 0.5,
        fill_color = colors_of_result[2],
        height=0.2, 
        width=0.4,
    ).next_to(legend_multiply_and_shift, DOWN).align_to(legend_multiply_and_shift, LEFT)
    legend_shift_and_separate_desc = Tex(
        ": Shift and Separate",
        font_size = 30
    ).next_to(legend_shift_and_separate, RIGHT)

    legend_shift_and_save = Rectangle(
        color=BLACK,
        fill_opacity = 0.5,
        fill_color = colors_of_result[2],
        height=0.2, 
        width=0.4,
    ).next_to(legend_shift_and_separate, DOWN).align_to(legend_shift_and_separate, LEFT)
    legend_shift_and_save_desc = Tex(
        ": Shift and Save",
        font_size = 30
    ).next_to(legend_shift_and_save, RIGHT)

    legend_tot = VGroup(
        legend_shape,
        legend_color,
        legend_triangle,
        legend_triangle_desc,
        legend_dot,
        legend_dot_desc,
        legend_color,
        legend_compact_bins,
        legend_compact_bins_desc,
        legend_multiply_and_shift,
        legend_multiply_and_shift_desc,
        legend_shift_and_separate,
        legend_shift_and_separate_desc,
        legend_shift_and_save,
        legend_shift_and_save_desc,
    ).align_on_border(RIGHT)

    self.play(
        AnimationGroup(
            FadeOut(chicago_results),
            Transform(shift_and_save_best, dot_taxi[3]),
            Transform(shift_and_separate_best, dot_taxi[2]),
            Transform(multiply_and_shift_best, dot_taxi[1]),
            Transform(compact_bin_best, dot_taxi[0]),
            Write(ax),
            FadeIn(y_label, x_label),
            Write(dashed_lines),
            lag_ratio=0.2,
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        FadeIn(legend_tot),
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        AnimationGroup(
            FadeIn(*triangle_uci,scale=1.5),
            lag_ratio=0.2,
        )
    )
    self.wait(0.1)
    self.next_slide()
    self.play(
        *[FadeOut(mob) for mob in self.mobjects if mob != self.title_of_the_paper]
        # All mobjects in the screen are saved in self.mobjects
    )
    self.wait(0.1)
    self.next_slide()

def thank_you(self):
    self.play(Write(Text("Thank you!", slant=ITALIC, ).scale(2)), run_time = 3.0)
    self.wait(0.1)
    self.next_slide()

class FullPresentation(Slide, MovingCameraScene):
    #config["frame_rate"] = 6
    def construct(self):    
        def place_at_the_top_of_frame(mobj):
            mobj.move_to(self.camera.frame_center + UP*(self.camera.frame_height/2)*0.88 )
            mobj.rescale_to_fit(self.camera.frame_width*0.8, 0)
            mobj.underline.set_stroke(width = self.camera.frame_height/10)   
        self.camera.frame.save_state() 
        self.camera.background_color = WHITE#"#edf2f4"
        self.color_list = [ RED, "#E3B505", "#654F6F", "#107E7D", "#FF784F",]
        Text.set_default(color=BLACK)
        BraceBetweenPoints.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        Square.set_default(color=BLACK)
        DashedLine.set_default(color=BLACK)
        Dot.set_default(color=BLACK)
        DoubleArrow.set_default(max_tip_length_to_length_ratio=0.5)
        self.title_of_the_paper = Title(
            "Lossless preprocessing of floating point data to enhance compression\\\\\
            F. Taurone, D. E. Lucani, M. Fehér, Q. Zhang -  Aarhus University, Denmark",
            stroke_color = BLACK, font_size = 35, underline_buff=SMALL_BUFF)
        self.title_of_the_paper.underline.set_color(BLACK)
        self.title_of_the_paper.move_to(self.camera.frame_center)
        
        self.play(Write(self.title_of_the_paper))
        self.wait(0.1)
        self.next_slide()
        self.play(
            self.title_of_the_paper.animate.move_to(self.camera.frame_center + UP*(self.camera.frame_height/2)*0.88 )
        )
        self.play(self.title_of_the_paper.animate.rescale_to_fit(self.camera.frame_width*0.8, 0))
        self.title_of_the_paper.add_updater(place_at_the_top_of_frame)
        self.wait(0.1)
        self.next_slide()
        #self.next_section(skip_animations=False)
        
        ### COMPRESSION
        compression(self)
        
        ### DEDUPLICATION
        deduplication(self)

        ### RELATED WORK
        related_work(self)

        ### COMPACT BIN
        compact_bins(self)
        
        ### MULTIPLY AND SHIFT
        multiply_and_shift(self)

        ### SHIFT AND SEPARATE EVEN FROM ODD
        shift_and_separate_even_from_odd(self)

        ### SHIFT AND SAVE EVENNESS
        shift_and_save_evenness(self)
        
        ### Results
        show_results(self)

        ### Thank You
        thank_you(self)

        self.wait()     