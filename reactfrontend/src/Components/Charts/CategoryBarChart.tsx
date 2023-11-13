import {useLayoutEffect, useState} from "react";
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Dark from "@amcharts/amcharts5/themes/Dark";

export default function CategoryBarChart(props:any){
    const [data, setData] = useState(null);

    useLayoutEffect(()=> {
        let root = am5.Root.new(props.chartID);
        root.setThemes([am5themes_Dark.new(root)])
        let chart = root.container.children.push(
            am5xy.XYChart.new(root, {
                panY: false,
                layout: root.verticalLayout
            })
        );

        // Define data

        // Create Y-axis
        let yAxis = chart.yAxes.push(
            am5xy.ValueAxis.new(root, {
                renderer: am5xy.AxisRendererY.new(root, {})
            })
        );
        yAxis.get("renderer").labels.template.setAll({
            fill:root.interfaceColors.get("text")
        });

        // Create X-Axis
        let xAxis = chart.xAxes.push(
            am5xy.CategoryAxis.new(root, {
                renderer: am5xy.AxisRendererX.new(root, {}),
                categoryField: "category"
            })
        );
        xAxis.data.setAll(props.chartData);
        xAxis.get("renderer").labels.template.setAll({
            fill:root.interfaceColors.get("text")
        });

        // Create series
        let series1 = chart.series.push(
            am5xy.ColumnSeries.new(root, {
                name: "Series",
                xAxis: xAxis,
                yAxis: yAxis,
                valueYField: "value1",
                categoryXField: "category"
            })
        );
        series1.data.setAll(props.chartData);

        let series2 = chart.series.push(
            am5xy.ColumnSeries.new(root, {
                name: "Series",
                xAxis: xAxis,
                yAxis: yAxis,
                valueYField: "value2",
                categoryXField: "category"
            })
        );
        series2.data.setAll(props.chartData);

        // Add legend
        let legend = chart.children.push(am5.Legend.new(root, {}));
        legend.data.setAll(chart.series.values);

        // Add cursor
        chart.set("cursor", am5xy.XYCursor.new(root, {},));
        return () => {root.dispose();};
    }, [props.chartID])
    return (<div className={props.class} id={props.chartID}></div>);
}