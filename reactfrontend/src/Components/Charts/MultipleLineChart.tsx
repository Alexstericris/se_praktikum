import React, {useLayoutEffect} from "react";
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Dark from "@amcharts/amcharts5/themes/Dark";

export default function MultipleLineChart(props: any){
    useLayoutEffect(()=> {
        let root = am5.Root.new(props.chartID);
        root.setThemes([am5themes_Dark.new(root)])
        let chart = root.container.children.push(
            am5xy.XYChart.new(root, {
                panX: true,
                panY: true,
                wheelX: "panX",
                wheelY: "zoomX",
                pinchZoomX:true
            })
        );

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
            am5xy.DateAxis.new(root, {
                baseInterval: { timeUnit: "millisecond", count: 1 },
                renderer: am5xy.AxisRendererX.new(root, {}),
            })
        );
        xAxis.data.setAll(props.chartData);
        xAxis.get("renderer").labels.template.setAll({
            fill:root.interfaceColors.get("text")
        });

        // Create series
        let series1 = chart.series.push(
            am5xy.LineSeries.new(root, {
                name: "Series",
                xAxis: xAxis,
                yAxis: yAxis,
                valueYField: "value",
                valueXField: "timestamp",
                stroke: am5.color('#87CEFA')
            })
        );
        series1.data.processor = am5.DataProcessor.new(root, {
            numericFields: ['value'],
        //     dateFields:["relative_time"],
        //     dateFormat: "yyyy-MM-dd"
        });
        series1.data.setAll(props.chartData);

        // let series2 = chart.series.push(
        //     am5xy.LineSeries.new(root, {
        //         name: "Series",
        //         xAxis: xAxis,
        //         yAxis: yAxis,
        //         valueYField: "value2",
        //         valueXField: "date"
        //     })
        // );
        // series2.data.processor = am5.DataProcessor.new(root, {
        //     numericFields: ['series2'],
        //     dateFields:["date"],
        //     dateFormat: "yyyy-MM-dd"
        // });
        // series2.data.setAll(props.chartData);

        // Add legend
        let legend = chart.children.push(am5.Legend.new(root, {}));
        legend.data.setAll(chart.series.values);


        // Add cursor
        chart.set("cursor", am5xy.XYCursor.new(root, {}));

        return () => {root.dispose();};
    }, [props.chartData])

    return <div className={props.class} id={props.chartID}></div>

}