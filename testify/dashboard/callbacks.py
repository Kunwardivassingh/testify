import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, no_update
from extensions import db
from models.test_data import TestData
import requests # Make sure to import the requests library
from urllib.parse import unquote
from flask_login import login_required  # <-- Add this import
def register_callbacks(dash_app):
    @login_required

    # --- Main Data Filtering Callback (Now with Real-Time and Manual Modes) ---
    @dash_app.callback(
        Output('filtered-data-store', 'data'),
        Output('error-message-store', 'data'), # New store for error messages
        Input('apply-filters-button', 'n_clicks'),
        Input('interval-component', 'n_intervals'), # <--- ADD THIS INPUT
        State('product-dropdown', 'value'),
        State('test-type-dropdown', 'value'),
        State('status-dropdown', 'value'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        State('url', 'search') # Read the URL query string
    )
    def update_data_store(n_clicks, n_intervals, products, test_types, statuses, start_date, end_date, search):
        # Determine the mode (manual vs. real-time) from the URL
        live_data_url = None
        if search:
            params = dict(x.split('=') for x in search.strip('?').split('&'))
            encoded_url = params.get('live_data_url')
            if encoded_url:
                live_data_url = unquote(encoded_url) # <--- ADD THIS LINE TO DECODE THE URL

        # --- Real-Time Mode ---
        if live_data_url:
            try:
                # Use pandas to directly read the CSV data from the provided URL
                df = pd.read_csv(live_data_url)
                
                 
                # --- ADD THIS FILTERING LOGIC FOR THE DATAFRAME ---
                # Convert execution_date to datetime for proper filtering
                df['execution_date'] = pd.to_datetime(df['execution_date'])

                if products:
                    df = df[df['product_name'].isin(products)]
                if test_types:
                    df = df[df['test_type'].isin(test_types)]
                if statuses:
                    df = df[df['status'].isin(statuses)]
                if start_date:
                    df = df[df['execution_date'] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df['execution_date'] <= pd.to_datetime(end_date)]
                # --- END OF NEW FILTERING LOGIC ---


                # Basic validation
                expected_columns = ['product_name', 'test_id', 'status']
                if not all(col in df.columns for col in expected_columns):
                    return no_update, {'error': "Invalid data format in the provided URL."}

                return df.to_json(date_format='iso', orient='split'), {'error': None}
            except Exception as e:
                return no_update, {'error': f"Failed to fetch or parse live data: {str(e)}"}

        # --- Manual (Database) Mode ---
        else:
            query = TestData.query
            if products:
                query = query.filter(TestData.product_name.in_(products))
            if test_types:
                query = query.filter(TestData.test_type.in_(test_types))
            if statuses:
                query = query.filter(TestData.status.in_(statuses))
            if start_date:
                query = query.filter(TestData.execution_date >= start_date)
            if end_date:
                query = query.filter(TestData.execution_date <= end_date)

            df = pd.read_sql(query.statement, db.get_engine())
            return df.to_json(date_format='iso', orient='split'), {'error': None}

    # --- Callback to Display Error Messages ---
    @dash_app.callback(
        Output('error-message-div', 'children'),
        Input('error-message-store', 'data')
    )
    def display_error_message(error_data):
        if error_data and error_data.get('error'):
            return html.Div(error_data['error'], className='error-message')
        return None

    # --- Dropdown and KPI Callbacks (No changes needed here) ---
    @dash_app.callback(
        [Output('product-dropdown', 'options'), Output('test-type-dropdown', 'options')],
        Input('apply-filters-button', 'n_clicks') # Trigger on initial load
    )
    def update_dropdowns(_):
        # Fetch distinct values for dropdowns from the database
        product_options = [{'label': p[0], 'value': p[0]} for p in db.session.query(TestData.product_name).distinct().all()]
        test_type_options = [{'label': t[0], 'value': t[0]} for t in db.session.query(TestData.test_type).distinct().all()]
        return product_options, test_type_options

    def create_kpi_callback(kpi_id, logic_function, title):
        @dash_app.callback(Output(kpi_id, 'children'), Input('filtered-data-store', 'data'))
        def update_kpi(jsonified_data):
            value = 0
            if jsonified_data:
                df = pd.read_json(jsonified_data, orient='split')
                if not df.empty:
                    value = logic_function(df)
            return [html.H4(title, className='card-title'), html.H2(f"{value:,}", className='card-value')]

    create_kpi_callback('kpi-total-tests', len, "Total Tests")
    create_kpi_callback('kpi-passed', lambda df: len(df[df['status'] == 'Pass']), "Passed")
    create_kpi_callback('kpi-failed', lambda df: len(df[df['status'] == 'Fail']), "Failed")
    create_kpi_callback('kpi-pending', lambda df: len(df[df['status'] == 'Pending']), "Pending")

    # --- Chart Callbacks (No changes needed here) ---
    chart_layout = {
        'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)', 'font_color': '#e0e0e0',
        'xaxis': {'gridcolor': '#444'}, 'yaxis': {'gridcolor': '#444'},
        'legend': {'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        'margin': dict(l=40, r=30, t=80, b=40)
    }

    @dash_app.callback(Output('results-over-time-graph', 'figure'), Input('filtered-data-store', 'data'))
    def update_line_chart(json_data):
        fig = go.Figure(layout=chart_layout)
        if not json_data: return fig
        df = pd.read_json(json_data, orient='split')
        df['execution_date'] = pd.to_datetime(df['execution_date'])
        data_over_time = df.groupby(df['execution_date'].dt.date).size().reset_index(name='count')
        fig = px.line(data_over_time, x='execution_date', y='count', title='Test Results Over Time')
        fig.update_layout(chart_layout)
        return fig

    @dash_app.callback(Output('status-pie-chart', 'figure'), Input('filtered-data-store', 'data'))
    def update_pie_chart(json_data):
        fig = go.Figure(layout=chart_layout)
        if not json_data: return fig
        df = pd.read_json(json_data, orient='split')
        status_counts = df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title='Test Status Distribution', hole=.3)
        fig.update_layout(chart_layout)
        return fig

    @dash_app.callback(Output('stacked-bar-chart', 'figure'), Input('filtered-data-store', 'data'))
    def update_stacked_bar_chart(json_data):
        fig = go.Figure(layout=chart_layout)
        if not json_data: return fig
        df = pd.read_json(json_data, orient='split')
        df_counts = df.groupby(['product_name', 'status']).size().reset_index(name='count')
        fig = px.bar(df_counts, x='product_name', y='count', color='status', title='Pass/Fail Rate by Product', barmode='stack')
        fig.update_layout(chart_layout)
        return fig

    @dash_app.callback(Output('duration-scatter-plot', 'figure'), Input('filtered-data-store', 'data'))
    def update_scatter_plot(json_data):
        fig = go.Figure(layout=chart_layout)
        if not json_data: return fig
        df = pd.read_json(json_data, orient='split')
        fig = px.scatter(df, x='execution_date', y='test_duration', color='status', title='Test Duration vs. Date')
        fig.update_layout(chart_layout)
        return fig

    @dash_app.callback(Output('duration-box-plot', 'figure'), Input('filtered-data-store', 'data'))
    def update_box_plot(json_data):
        fig = go.Figure(layout=chart_layout)
        if not json_data: return fig
        df = pd.read_json(json_data, orient='split')
        fig = px.box(df, x='test_type', y='test_duration', color='test_type', title='Test Duration Variability')
        fig.update_layout(chart_layout)
        return fig

    @dash_app.callback(Output('tester-donut-chart', 'figure'), Input('filtered-data-store', 'data'))
    def update_donut_chart(json_data):
        fig = go.Figure(layout=chart_layout)
        if not json_data: return fig
        df = pd.read_json(json_data, orient='split')
        tester_counts = df['test_type'].value_counts()
        fig = px.pie(values=tester_counts.values, names=tester_counts.index, title='Workload by Test Type', hole=.5)
        fig.update_layout(chart_layout)
        return fig

    @dash_app.callback(Output('coverage-area-chart', 'figure'), Input('filtered-data-store', 'data'))
    def update_area_chart(json_data):
        fig = go.Figure(layout=chart_layout)
        if not json_data: return fig
        df = pd.read_json(json_data, orient='split')
        df['execution_date'] = pd.to_datetime(df['execution_date']).dt.date
        df_cumulative = df.groupby('execution_date').size().cumsum().reset_index(name='cumulative_tests')
        fig = px.area(df_cumulative, x='execution_date', y='cumulative_tests', title='Cumulative Test Coverage')
        fig.update_layout(chart_layout)
        return fig

    @dash_app.callback(Output('execution-heatmap', 'figure'), Input('filtered-data-store', 'data'))
    def update_heatmap(json_data):
        fig = go.Figure(layout=chart_layout)
        if not json_data: return fig
        df = pd.read_json(json_data, orient='split')
        df['day_of_week'] = pd.to_datetime(df['execution_date']).dt.day_name()
        heatmap_data = df.groupby(['day_of_week', 'product_name']).size().reset_index(name='count')
        heatmap_pivot = heatmap_data.pivot(index='day_of_week', columns='product_name', values='count').fillna(0)
        fig = px.imshow(heatmap_pivot, text_auto=True, aspect="auto", title="Test Execution Frequency")
        fig.update_layout(chart_layout)
        return fig

    @dash_app.callback(Output('detailed-test-table', 'data'), Input('filtered-data-store', 'data'))
    def update_table(json_data):
        if not json_data: return []
        df = pd.read_json(json_data, orient='split')
        df['duration_str'] = df['test_duration'].apply(lambda x: f"{int(x // 60)}m {int(x % 60)}s" if pd.notna(x) else 'N/A')
        df['execution_date_str'] = pd.to_datetime(df['execution_date']).dt.strftime('%Y-%m-%d')
        return df.to_dict('records')

    # --- Export and Profile Callbacks (No changes needed) ---
    @dash_app.callback(
        Output("download-dataframe-csv", "data"),
        Input("export-csv-button", "n_clicks"),
        State("filtered-data-store", "data"),
        prevent_initial_call=True,
    )
    def export_csv(n_clicks, json_data):
        if not json_data: return None
        df = pd.read_json(json_data, orient='split')
        return dcc.send_data_frame(df.to_csv, "test_insights_export.csv", index=False)

    dash_app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0) {
                var menu = document.getElementById('dropdown-menu');
                menu.style.display = (menu.style.display === 'none' || menu.style.display === '') ? 'block' : 'none';
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output('profile-icon', 'n_clicks_timestamp'),
        Input('profile-icon', 'n_clicks')
    )

    dash_app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0) {
                const { jsPDF } = window.jspdf;
                const sourceElement = document.getElementById('dashboard-content-area');

                // --- THE PROFESSIONAL FIX: CLONE THE ELEMENT ---
                // 1. Create a clone of the element to be captured
                const clone = sourceElement.cloneNode(true);

                // 2. Style the clone for printing: off-screen, full-width, auto-height
                clone.style.position = 'absolute';
                clone.style.top = '-9999px';
                clone.style.left = '0px';
                clone.style.width = sourceElement.offsetWidth + 'px'; // Use the same width as the original
                clone.style.height = 'auto'; // Let it expand to its full content height
                clone.style.overflow = 'visible'; // Ensure no internal scrolling clips the content

                // Append the clone to the body so it can be rendered off-screen
                document.body.appendChild(clone);

                // Use a small timeout to allow the browser to render the full clone
                setTimeout(() => {
                    html2canvas(clone, {
                        backgroundColor: '#1a1c2c',
                        scale: 2,
                        useCORS: true,
                        // Tell html2canvas to use the clone's full scroll dimensions
                        width: clone.scrollWidth,
                        height: clone.scrollHeight
                    }).then(canvas => {
                        const imgData = canvas.toDataURL('image/png');
                        const pdf = new jsPDF({
                            orientation: 'landscape',
                            unit: 'mm',
                            format: 'a4'
                        });

                        const pdfWidth = pdf.internal.pageSize.getWidth();
                        const pdfHeight = pdf.internal.pageSize.getHeight();
                        const imgHeight = canvas.height * pdfWidth / canvas.width;
                        let heightLeft = imgHeight;
                        let position = 0;

                        pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, imgHeight);
                        heightLeft -= pdfHeight;

                        // Add new pages if the content is longer than one page
                        while (heightLeft > 0) {
                            position -= pdfHeight;
                            pdf.addPage();
                            pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, imgHeight);
                            heightLeft -= pdfHeight;
                        }

                        pdf.save('dashboard-export.pdf');

                    }).finally(() => {
                        // 4. CRITICAL: Remove the clone from the DOM after capture
                        document.body.removeChild(clone);
                    });
                }, 200); // 200ms delay for rendering
            }
            return '';
        }
        """,
        Output('export-pdf-button', 'n_clicks_timestamp'),
        Input('export-pdf-button', 'n_clicks')
    )
    @dash_app.callback(
        Output('profile-icon', 'n_clicks'),
        Input('profile-icon', 'n_clicks')
    )
    def reset_profile_icon(n_clicks):
        # This callback can be used to reset or handle profile icon clicks
        return n_clicks
    
    #            # --- DEFINITIVE, FINAL, SINGLE-PAGE PDF Export Clientside Callback ---
#     dash_app.clientside_callback(
#         """
#         function(n_clicks) {
#             if (n_clicks > 0) {
#                 const { jsPDF } = window.jspdf;
#                 const elementToCapture = document.getElementById('dashboard-content-area');
#                 const mainContent = document.querySelector('.main-content');
#                 const body = document.body;

#                 // 1. Store all original styles that will be changed
#                 const originalStyles = {
#                     body: { overflow: body.style.overflow, height: body.style.height },
#                     mainContent: { overflow: mainContent.style.overflow },
#                     element: { overflowY: elementToCapture.style.overflowY, height: elementToCapture.style.height }
#                 };
                
#                 // 2. Temporarily change styles on ALL parent containers to render the full content
#                 body.style.overflow = 'visible';
#                 body.style.height = 'auto';
#                 mainContent.style.overflow = 'visible';
#                 elementToCapture.style.overflowY = 'visible';
#                 elementToCapture.style.height = 'auto';

#                 // Use a timeout to ensure the browser has time to apply the new styles and re-render
#                 setTimeout(() => {
#                     html2canvas(elementToCapture, {
#                         backgroundColor: '#1a1c2c',
#                         scale: 2, // For higher resolution
#                         logging: true,
#                         useCORS: true
#                     }).then(canvas => {
#                         const imgData = canvas.toDataURL('image/png');
#                         const canvasWidth = canvas.width;
#                         const canvasHeight = canvas.height;
                        
#                         // --- THE SINGLE-PAGE FIX ---
#                         // Calculate the aspect ratio
#                         const ratio = canvasHeight / canvasWidth;
#                         // Define a fixed width for the PDF (e.g., A4 landscape width in mm)
#                         const pdfWidth = 297; 
#                         // Calculate the exact height the PDF needs to be to fit the entire image
#                         const pdfHeight = pdfWidth * ratio;

#                         // Create a new PDF with a CUSTOM format size, not a fixed one like 'a4'
#                         const pdf = new jsPDF({
#                             orientation: 'landscape',
#                             unit: 'mm',
#                             format: [pdfWidth, pdfHeight]
#                         });
                        
#                         // Add the image to the single, perfectly-sized page
#                         pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
                        
#                         // The multi-page 'while' loop is completely removed.
                        
#                         pdf.save('dashboard-export.pdf');

#                     }).finally(() => {
#                         // 3. CRITICAL: Restore all original styles to return the page to normal
#                         body.style.overflow = originalStyles.body.overflow;
#                         body.style.height = originalStyles.body.height;
#                         mainContent.style.overflow = originalStyles.mainContent.overflow;
#                         elementToCapture.style.overflowY = originalStyles.element.overflowY;
#                         elementToCapture.style.height = originalStyles.element.height;
#                     });
#                 }, 200); // A small delay is crucial for rendering
#             }
#             return '';
#         }
#         """,
#         Output('export-pdf-button', 'n_clicks_timestamp'),
#         Input('export-pdf-button', 'n_clicks')
#     )

