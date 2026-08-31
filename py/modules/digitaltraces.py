# py/modules/digitaltraces.py
import datashader as ds
import datashader.transfer_functions as tf
from datashader.colors import rgb
from datashader.utils import lnglat_to_meters
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, Optional
import dask.diagnostics as diag

DE_BOUNDS = ((4.605469, 16.37207), (46.697243, 55.685885))

def query_region(con, parquet_dir, bounds):
    """Queries DuckDB for points within a WGS84 bounding box."""
    xs, ys = lnglat_to_meters([bounds[0][0], bounds[0][1]], [bounds[1][0], bounds[1][1]])
    
    query = f"""
        SELECT x, y, classification
        FROM '{parquet_dir}/*.parquet'
        WHERE x BETWEEN {xs[0]} AND {xs[1]}
          AND y BETWEEN {ys[0]} AND {ys[1]}
    """
    df = con.execute(query).df()
    if not df.empty:
        df['classification'] = df['classification'].astype('category')
    return df

def create_bordered_map_alpha(
    df, bounds: Tuple[Tuple[float, float]], border_gdf, color_key, background='white',
    plot_width=1200, local_weight=1.0, return_raster: Optional[bool] = None
):
    """Creates a high-resolution static map of categorical point data."""
    x_range, y_range = bounds
    x_coords, y_coords = lnglat_to_meters(x_range, y_range)
    
    # Exact Aspect Ratio to eliminate Matplotlib whitespace
    x_width_m = x_coords[1] - x_coords[0]
    y_height_m = y_coords[1] - y_coords[0]
    plot_height = int(plot_width * (y_height_m / x_width_m))
    
    cvs = ds.Canvas(
        plot_width=plot_width, plot_height=plot_height,
        x_range=x_coords, y_range=y_coords
    )

    with diag.ProgressBar():
        agg = cvs.points(df, x='x', y='y', agg=ds.by('classification'))

    cats = list(agg.coords['classification'].values)
    weighted_agg = agg.astype(np.float64)

    if local_weight != 1.0 and 'Local' in cats:
        local_idx = cats.index('Local')
        weighted_agg.data[:, :, local_idx] *= local_weight

    majority_indices = weighted_agg.argmax(dim='classification')
    original_total_counts = agg.sum(dim='classification')
    data_mask = original_total_counts.data > 0

    img_alpha = tf.shade(original_total_counts, cmap="white", how='eq_hist')
    alpha_channel = np.nan_to_num(img_alpha.data, nan=0).astype(np.uint8)

    bg_color_tuple = rgb(background)
    final_rgba = np.full((plot_height, plot_width, 4), list(bg_color_tuple) + [255], dtype=np.uint8)

    for i, cat in enumerate(cats):
        if cat in color_key:
            mask = (majority_indices.data == i) & data_mask
            final_rgba[mask, :3] = rgb(color_key[cat])

    final_rgba[data_mask, 3] = alpha_channel[data_mask]
    
    # Wrap in tf.Image just for Matplotlib compatibility
    final_image = tf.Image(final_rgba)

    # Dynamic Figure Size based on exact aspect ratio
    fig_w = 12.0
    fig_h = fig_w * (plot_height / plot_width)
    fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h), facecolor=background)

    # interpolation='nearest' ensures the 1-pixel dots aren't blurred by the browser!
    ax.imshow(
        final_image.to_pil(),
        extent=[x_coords[0], x_coords[1], y_coords[0], y_coords[1]],
        interpolation='nearest'
    )

    border_gdf.to_crs(epsg=3857).plot(
        ax=ax, facecolor='none', edgecolor='black', linewidth=0.5, alpha=0.7
    )
    ax.set_xlim(x_coords)
    ax.set_ylim(y_coords)
    ax.set_axis_off()

    if return_raster:
        return fig, final_image
    return fig

def render_datashader_map(df, bounds, border, title="Digital Traces"):
    if df.empty:
        print(f"No data to plot for {title}.")
        return plt.subplots()[0]

    color_key = {'Local': 'blue', 'Tourist': 'red', 'Unclassified': 'cornflowerblue'}
    opts = {
        "df": df, "bounds": bounds, "border_gdf": border,
        "color_key": color_key, "background": 'white',
        "plot_width": 1200, "local_weight": 1.0, 
        "return_raster": True,
    }
    
    fig, img_fg = create_bordered_map_alpha(**opts)
    ax = fig.axes[0]
    ax.set_title(title, fontsize=18, pad=10)
    fig.tight_layout()
    
    return fig