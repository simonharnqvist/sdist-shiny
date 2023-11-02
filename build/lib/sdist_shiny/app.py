from shiny import ui, render, App
from shiny.types import ImgData
import pandas as pd
import seaborn as sns
from dismal.likelihood import expected_s

app_ui = ui.page_fluid(
                       ui.h3("Segregating sites distribution"),
                       ui.output_image("image"),
                        
    ui.row(
        ui.column(
            3,
            ui.strong("Thetas (per site)"),
            ui.input_slider("theta1", "θ_1", value=0.04, min=0, max=1, step=0.01),
            ui.input_slider("theta2", "θ_2", value=0.04, min=0, max=1, step=0.01),
            ui.input_slider("theta3", "θ_3", value=0.04, min=0, max=1, step=0.01),
            ui.input_slider("theta4", "θ_4", value=0.04, min=0, max=1, step=0.01),
            ui.input_slider("theta5", "θ_5", value=0.04, min=0, max=1, step=0.01),
        ),
        ui.column(
            3,
            ui.strong("Epoch durations (2 Ne generations)"),
            ui.input_slider("t1", "T_1", min=0, max=10, value=1, step=0.1),
            ui.input_slider("t2", "T_2", min=0, max=10, value=1, step=0.1),
        ),
        ui.column(
            3,
            ui.strong("Migration rates (migrants per generations)"),
            ui.input_slider("mig1", "M_12", min=0, max=5, value=0, step=0.05),
            ui.input_slider("mig2", "M_21", min=0, max=5, value=0, step=0.05),
            ui.input_slider("mig3", "M_34", min=0, max=5, value=0, step=0.05),
            ui.input_slider("mig4", "M_43", min=0, max=5, value=0, step=0.05),
        ),),
        ui.row(ui.input_numeric("blocklen", ui.strong("Block length"), 500, min=0, max=10000),
            ui.input_numeric("cutoff", ui.strong("S cutoff"), 20, min=1, max=1000)),
        ui.row(ui.output_plot("hist")
    ),
    title="Segregating sites distribution",)


def server(input, output, session):

    @output
    @render.image
    def image():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "gim_params.png"), "width":"400px"}
        return img

    @output
    @render.plot
    def hist():
        block_thetas = [theta * input.blocklen() for theta in [input.theta1(), input.theta2(), input.theta3(), input.theta4(), input.theta5()]]

        state1, state2, state3 = [expected_s(state=i,
                            thetas = block_thetas,
                                      epoch_durations=[input.t1(), input.t2()],
                                      mig_rates=[input.mig1(), input.mig2(), input.mig3(), input.mig4()],
                                      cutoff=input.cutoff()) 
                                      for i in [1,2,3]]
        
        df = pd.DataFrame({"state_1": state1, "state_2": state2, "state_3":state3})
        df["s"] = df.index
        df = df.melt(id_vars=["s"], var_name="state", value_name="Pr(S)")
    
        g = sns.lineplot(df, x="s", y="Pr(S)", hue="state")
        g.set(xlabel = "Number of segregating sites", ylabel="Density", xticks=[i for i in range(0, input.cutoff()+1, 5)])
        return g
    

app = App(app_ui, server)