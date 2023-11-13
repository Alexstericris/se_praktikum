import {NodeTypeConfig} from "flume/dist/types";

export const filterNodes: NodeTypeConfig[] = [
    {
        type: "clipping_filter",
        label: "Function: Clipping Filter",
        inputs: ports =>
            [
                ports["data"](),
                ports["float"]({label: "max", name: "max"}),
                ports["float"]({label: "min", name: "min"}),
            ],
        outputs:ports => [
            ports["data"]()
        ]
    },
    {
        type: "interpolate_nan",
        label: "Function: Lerp Missing",
        inputs: ports =>
            [
                ports["data"](),
                ports["selectNulltype"]()
            ],
        outputs:ports => [
            ports["data"]()
        ]
    },
    {
        type: "moving_average",
        label: "Function: Moving Average",
        inputs: ports =>
            [
                ports["data"](),
                ports["string"]({label:"kernel", name:"kernel"})
            ],
        outputs:ports => [
            ports["data"]()
        ]
    },
    {
        type: "adaptive_smoothing",
        label: "Function: Adaptive Smoothing",
        inputs: ports =>
            [
                ports["data"](),
                ports["integer"]({label:"window_size", name:"window_size"})
            ],
        outputs:ports => [
            ports["data"]()
        ]
    },
    {
        type: "peak_removal",
        label: "Function: Peak Removal",
        inputs: ports =>
            [
                ports["data"](),
                ports["integer"]({label:"repeat", name:"repeat"})
            ],
        outputs:ports => [
            ports["data"]()
        ]
    },
    {
        type: "derivative_smoothing",
        label: "Function: Derivative Smoothing",
        inputs: ports =>
            [
                ports["data"](),
                ports["kernel"]({label:"kernel", name:"kernel"})
            ],
        outputs:ports => [
            ports["data"]()
        ]
    },
    {
        type: "resampling_nearest",
        label: "Function: Resample Nearest",
        inputs: ports =>
            [
                ports["data"](),
                ports["kernel"]({label:"x_values", name:"x_values"})
            ],
        outputs:ports => [
            ports["data"]()
        ]
    },
    {
        type: "resampling_linear",
        label: "Function: Linear Resampling",
        inputs: ports =>
            [
                ports["data"](),
                ports["kernel"]({label:"kernel", name:"kernel"}),
                ports["float"]({label: "left", name: "left"}),
                ports["float"]({label: "right", name: "right"})
            ],
        outputs:ports => [
            ports["data"]()
        ]
    },

]