import plotly.express as px
import plotly
import pandas as pd
from domain_to_ga import AssignmentGene


def visualize(solution: list[AssignmentGene]):
    df = pd.DataFrame(
        [
            {
                "Assignment": gene.assignment.name,
                "from": gene.assignment.start_date,
                "to": gene.deadline,
                "hours_to_complete": f"hours_to_complete: {gene.assignment.hours_to_complete}",
            }
            for gene in solution
        ]
    )
    fig = px.timeline(
        data_frame=df,
        x_start="from",
        x_end="to",
        y="Assignment",
        color="Assignment",
        labels="Assignment",
        text="hours_to_complete",
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(font=plotly.graph_objs.layout.Font(size=22))
    fig.show()
