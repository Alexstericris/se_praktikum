import {useLayoutEffect, useState} from "react";
import * as am5 from "@amcharts/amcharts5";
import * as am5percent from "@amcharts/amcharts5/percent";
import am5themes_Dark from "@amcharts/amcharts5/themes/Dark";

export default function PieChart(props: any){
    const [data, setData] = useState(null);
    useLayoutEffect(()=> {
        let root = am5.Root.new(props.chartID);
        root.setThemes([am5themes_Dark.new(root)])
        let chart = root.container.children.push(
            am5percent.PieChart.new(root, {
                layout: root.verticalLayout
            })
        );

        // Create series
        let series = chart.series.push(
            am5percent.PieSeries.new(root, {
                name: "Series",
                valueField: "value",
                categoryField: "category"
            })
        );
        series.data.setAll(props.chartData);
        // Add legend
        let legend = chart.children.push(am5.Legend.new(root, {}));
        legend.data.setAll(chart.series.values);

        // Add cursor
        return () => {root.dispose();};
    }, [props.chartID])

    return (<div className={"piechart"} id={props.chartID}></div>)
}