from shiny import ui, render, App
from shiny.types import ImgData
import pandas as pd
import matplotlib.pyplot as plt
from dismal.model_instance import ModelInstance
from dismal.demography import Epoch

app_ui = ui.page_fluid(
                           ui.column(
        10,
        {"class": "col-md-10 col-lg-8 py-5 mx-auto text-lg-center text-left"},
        ui.h1("Visualise the segregating sites distribution under different demographic scenarios"),
    ),
                       ui.layout_sidebar(
                           ui.sidebar(
                               ui.strong("Thetas (per site)"),
                               ui.input_slider("theta1", "θ_1", value=0.01, min=0, max=1, step=0.01),
                               ui.input_slider("theta2", "θ_2", value=0.01, min=0, max=1, step=0.01),
                               ui.input_slider("theta3", "θ_3", value=0.01, min=0, max=1, step=0.01),
                               ui.input_slider("theta4", "θ_4", value=0.01, min=0, max=1, step=0.01),
                               ui.input_slider("theta5", "θ_5", value=0.01, min=0, max=1, step=0.01),
                               ui.strong("Epoch durations (2 Ne generations)"),
                               ui.help_text("Set T_2 to zero to remove middle epoch"),
                               ui.input_slider("t1", "T_1", min=0, max=10, value=1, step=0.1),
                               ui.input_slider("t2", "T_2", min=0, max=10, value=1, step=0.1),
                               ui.strong("Migration rates (migrants per generation)"),
                               ui.input_slider("mig1", "M_12", min=0, max=5, value=0, step=0.05),
                               ui.input_slider("mig2", "M_21", min=0, max=5, value=0, step=0.05),
                               ui.input_slider("mig3", "M_34", min=0, max=5, value=0, step=0.05),
                               ui.input_slider("mig4", "M_43", min=0, max=5, value=0, step=0.05),
                           ),
                           ui.card(
                               ui.card_header("Model parameters"),
                               ui.output_image("image"),
                               full_screen=True,
                           ),
                            ui.row(ui.input_numeric("blocklen", ui.strong("Block length"), 100, min=1, max=10000),
                            ui.input_numeric("cutoff", ui.strong("S cutoff"), 30, min=1, max=1000)),
                           ui.card(
                               ui.card_header("Segregating sites spectrum"),
                               ui.output_plot("plot_sdist"),
                                  ),
                       ))



def server(input, output, session):
    
    @output
    @render.plot
    def plot_sdist():

        epochs = [Epoch(deme_ids=("epoch1_pop1", "epoch1_pop2"), migration=True)]
        epochs.append(Epoch(deme_ids=("epoch2_pop1", "epoch2_pop2"), migration=True))
        epochs.append(Epoch(deme_ids=("epoch3_pop",), migration=False))

        params = [theta * input.blocklen() 
                        for theta in [input.theta1(), 
                                      input.theta2(), 
                                      input.theta3(), 
                                      input.theta4(), 
                                      input.theta5()]]
        
        params.extend([input.t1(), input.t2(), 
                                            input.mig1(), input.mig2(), 
                                            input.mig3(), input.mig4()])
        
        mod = ModelInstance(params, epochs)

        s1, s2, s3 = [mod.expected_s1(s_max=input.cutoff()), 
                      mod.expected_s2(s_max=input.cutoff()), 
                      mod.expected_s3(s_max=input.cutoff())]
        
        s = list(range(input.cutoff()+1))
        
        fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharex=True, sharey=True)
        ax1.bar(s, s1)
        ax2.bar(s, s2)
        ax3.bar(s, s3)
        ax1.set_title("S1 (within population 1)", fontsize=25)
        ax2.set_title("S2 (within population 2)", fontsize=25)
        ax3.set_title("S3 (between populations)", fontsize=25)

        fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.xlabel("s", fontsize=40)
        plt.ylabel("Pr(S=s)", fontsize=25)

        
        return fig


    @output
    @render.image
    def image():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "gim_params.png"), "width":"700px", "style":"display: block; margin-left: auto; margin-right: auto;"}
        return img


app = App(app_ui, server)

