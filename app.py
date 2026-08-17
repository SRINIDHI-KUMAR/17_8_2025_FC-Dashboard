import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Freight Cost Dashboard", layout="wide")

def get_theme_mode():
    try:
        t = st.context.theme
        if t is not None and getattr(t, "type", None) in ("light", "dark"):
            return t.type
    except Exception:
        pass
    try:
        base = st.get_option("theme.base")
        if base in ("light", "dark"):
            return base
    except Exception:
        pass
    return "dark"

def chart_tokens(mode):
    if mode == "dark":
        return {"text":"#FFFFFF","title":"#FFFFFF","axis":"rgba(255,255,255,0.82)",
                "grid":"rgba(255,255,255,0.10)","bg":"rgba(0,0,0,0)"}
    return {"text":"#1C0A2E","title":"#1C0A2E","axis":"rgba(28,10,46,0.85)",
            "grid":"rgba(28,10,46,0.12)","bg":"rgba(0,0,0,0)"}

def get_series(mode):
    if mode == "dark":
        return {"dedi":"#4CAF50","market":"#F44336","idt":"#FF9800",
                "ly":"#4CAF50","proj":"#F44336","cy":"#2196F3"}
    return {"dedi":"#2E7D32","market":"#C62828","idt":"#E65100",
            "ly":"#2E7D32","proj":"#C62828","cy":"#1565C0"}

def apply_custom_css(mode):
    if mode == "dark":
        app_bg="radial-gradient(1200px 820px at 18% -5%, #46195a 0%, #380b3a 48%, #29082d 100%)"
        heading="#FFFFFF"; card_grad="linear-gradient(135deg, #5a2b86 0%, #3c1257 100%)"
        card_border="rgba(255,255,255,0.14)"
        card_shadow="0 6px 18px rgba(0,0,0,0.40), inset 0 1px 0 rgba(255,255,255,0.06)"
        metric_label="#E5D6F5"; metric_value="#FFFFFF"; body_text="#F3EAFB"
    else:
        app_bg="radial-gradient(1200px 820px at 18% -5%, #F5ECFC 0%, #ECE0F7 52%, #E1D0F1 100%)"
        heading="#1C0A2E"; card_grad="linear-gradient(135deg, #EFE3FA 0%, #DFCCF1 100%)"
        card_border="rgba(74,26,107,0.25)"
        card_shadow="0 6px 16px rgba(74,26,107,0.12), inset 0 1px 0 rgba(255,255,255,0.65)"
        metric_label="#4A1A6B"; metric_value="#1C0A2E"; body_text="#1C0A2E"

    light_fix = "" if mode == "dark" else """
        .block-container, .block-container p, .block-container label,
        .block-container span, .block-container li, .block-container small,
        .block-container h1, .block-container h2, .block-container h3,
        .block-container [data-testid="stMarkdownContainer"],
        .block-container [data-testid="stMarkdownContainer"] *,
        .block-container [data-testid="stWidgetLabel"] p,
        .block-container [data-testid="stFileUploaderDropzoneInstructions"] *,
        .block-container [data-testid="stFileName"],
        [data-testid="stMain"] p, [data-testid="stMain"] label,
        [data-testid="stMain"] span, [data-testid="stMain"] li,
        [data-testid="stFileUploaderDropzoneInstructions"] * { color:#1C0A2E !important; }
        .block-container [data-testid="stFileName"],
        [data-testid="stFileUploaderFileData"] small { color:#3A1A4D !important; }
    """

    st.markdown(f"""
    <style>
        .stApp {{ background: {app_bg} !important; }}
        [data-testid="stHeader"] {{ background: transparent !important; }}
        .stApp, .stApp p, .stApp label, .stApp span {{ color: {body_text}; }}
        h1, h2, h3 {{ color: {heading} !important; font-weight: 700 !important; letter-spacing: -0.2px; }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(160deg, #2d0a2f 0%, #380b3a 55%, #4a1a6b 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.10) !important; }}
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] label p,
        section[data-testid="stSidebar"] label span,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {{ color: #FFFFFF !important; }}
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] .stSelectbox label {{ font-size: 0.75rem !important; }}
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{ gap: 0.5rem !important; }}
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
            background-color: rgba(255,255,255,0.05) !important; padding: 0.3rem 0.8rem !important;
            border-radius: 8px !important; border: 1px solid rgba(255,255,255,0.10) !important; color: #FFFFFF !important; }}
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-selected="true"] {{
            background-color: #7D4BAE !important; border-color: rgba(255,255,255,0.32) !important; color: #FFFFFF !important; }}

        section[data-testid="stSidebar"] div[data-baseweb="select"],
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
            background-color: #FFFFFF !important; border-radius: 8px !important;
            border: 1px solid rgba(0,0,0,0.18) !important; min-height: 2.2rem !important; }}
        section[data-testid="stSidebar"] div[data-baseweb="select"] *,
        section[data-testid="stSidebar"] div[data-baseweb="select"] div,
        section[data-testid="stSidebar"] div[data-baseweb="select"] span,
        section[data-testid="stSidebar"] div[data-baseweb="select"] p,
        section[data-testid="stSidebar"] div[data-baseweb="select"] input,
        section[data-testid="stSidebar"] div[data-baseweb="select"] svg,
        section[data-testid="stSidebar"] div[data-baseweb="select"] path,
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] * {{
            color: #1C0A2E !important; -webkit-text-fill-color: #1C0A2E !important; fill: #1C0A2E !important; opacity: 1 !important; }}
        [data-testid="stSelectboxVirtualDropdown"],
        [data-testid="stSelectboxVirtualDropdown"] *,
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] *,
        div[data-baseweb="popover"] ul[role="listbox"],
        ul[role="listbox"], ul[role="listbox"] li, [role="option"] {{
            background-color: #FFFFFF !important; color: #1C0A2E !important; -webkit-text-fill-color: #1C0A2E !important; }}
        ul[role="listbox"] li *, [role="option"] * {{
            color: #1C0A2E !important; -webkit-text-fill-color: #1C0A2E !important; }}
        [role="option"]:hover, [role="option"][aria-selected="true"],
        [role="option"]:hover *, [role="option"][aria-selected="true"] * {{
            background-color: #EDE1F7 !important; color: #1C0A2E !important; -webkit-text-fill-color: #1C0A2E !important; }}

        div[data-testid="stMetric"] {{
            background: {card_grad} !important; padding: 0.7rem 0.9rem !important;
            border-radius: 14px !important; border: 1px solid {card_border} !important;
            box-shadow: {card_shadow} !important; }}
        div[data-testid="stMetricLabel"] p {{
            font-size: 0.66rem !important; font-weight: 700 !important; text-transform: uppercase;
            letter-spacing: 0.6px; color: {metric_label} !important; }}
        div[data-testid="stMetricValue"] {{
            font-size: 1.25rem !important; font-weight: 800 !important; color: {metric_value} !important; }}

        hr {{ border-color: {card_border} !important; }}
        .block-container {{ padding-top: 2rem !important; padding-bottom: 0.2rem !important;
            padding-left: 1.1rem !important; padding-right: 1.1rem !important; }}
        {light_fix}
    </style>
    """, unsafe_allow_html=True)

def fmt(v):
    if v is None or pd.isna(v):
        return ""
    return f"{float(v):,.2f}"

def _hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _mix(c1, c2, t):
    return tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def _shade(base_hex, t):
    base = _hex_to_rgb(base_hex)
    dark = _mix(base, (0, 0, 0), 0.35)
    light = _mix(base, (255, 255, 255), 0.25)
    r, g, b = _mix(dark, light, t)
    return f"rgb({r},{g},{b})"

def add_gradient_bars(fig, x, values, base_hex, tok, row=None, col=None, n=12,
                      width=0.6, offsetgroup=None, show_text=True, text_size=11):
    xs = list(x)
    vals = [float(v) if (v is not None and not pd.isna(v)) else 0.0 for v in values]
    bases = list(base_hex) if isinstance(base_hex, (list, tuple)) else [base_hex] * len(xs)
    for k in range(n):
        t = k / (n - 1) if n > 1 else 1.0
        top = (k == n - 1)
        colors = [_shade(bases[j], t) for j in range(len(xs))]
        kwargs = dict(
            x=xs, y=[v / n for v in vals],
            marker=dict(color=colors, line=dict(width=0)),
            width=width, offsetgroup=offsetgroup, showlegend=False,
            customdata=vals, cliponaxis=False,
            hovertemplate="%{x}<br>%{customdata:,.2f}<extra></extra>",
            text=[fmt(v) if (top and show_text and v != 0) else '' for v in vals],
            textposition='outside',
            textfont=dict(color=tok['text'], size=text_size, weight='bold'),
        )
        if not top:
            kwargs['hoverinfo'] = 'skip'
        tr = go.Bar(**kwargs)
        if row:
            fig.add_trace(tr, row=row, col=col)
        else:
            fig.add_trace(tr)

def legend_swatch(fig, name, base_hex, x0, row=None, col=None):
    tr = go.Bar(x=[x0], y=[None], marker_color=_shade(base_hex, 0.5),
                name=name, showlegend=True)
    if row:
        fig.add_trace(tr, row=row, col=col)
    else:
        fig.add_trace(tr)

KNOWN_DEPOTS = {'VIJAYAWADA','COIMBATORE','HUBLI','COCHIN','HYDERABAD','CHENNAI','BANGALORE'}

def parse_sec_summary(df_summary):
    month_list=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_rows=df_summary[df_summary.iloc[:,0].astype(str).str.strip().isin(month_list)].copy()
    if month_rows.empty:
        st.error("No month rows found in Sec Summary."); return pd.DataFrame()
    month_rows=month_rows.iloc[:12]
    cols_ly=[1,2,3,4,5,6]; cols_proj=[7,8,9,10,11,12]; cols_cy=[13,14,15,16,17,18]; cols_cyproj=[19,20,21,22,23,24]
    data=[]
    for _,row in month_rows.iterrows():
        data.append([row.iloc[0]]+list(row.iloc[cols_ly].values)+list(row.iloc[cols_proj].values)+
                    list(row.iloc[cols_cy].values)+list(row.iloc[cols_cyproj].values))
    columns=['Month','LY_Dedi','LY_Market','LY_IDT','LY_TotalFRT','LY_Vol','LY_RPT',
             'Proj_Dedi','Proj_Market','Proj_IDT','Proj_TotalFRT','Proj_Vol','Proj_RPT',
             'CY_Dedi','CY_Market','CY_IDT','CY_TotalFRT','CY_Vol','CY_RPT',
             'CYProj_Dedi','CYProj_Market','CYProj_IDT','CYProj_TotalFRT','CYProj_Vol','CYProj_RPT']
    df=pd.DataFrame(data,columns=columns)
    for col in df.columns:
        if col!='Month': df[col]=pd.to_numeric(df[col],errors='coerce')
    return df

def parse_sec_detailed(df_detailed):
    month_list=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_row_indices=[0,12,24,36,48,60,72,84,96,108,120,132]
    df=df_detailed.reset_index(drop=True)
    month_indices=[]
    for idx in month_row_indices:
        if idx<len(df) and df.shape[1]>1:
            val=str(df.iloc[idx,1]).strip()
            if val in month_list: month_indices.append((idx,val))
    if not month_indices:
        st.error("No month blocks found."); return pd.DataFrame()
    all_data=[]
    for bi,(sr,month) in enumerate(month_indices):
        ds=sr+2; er=month_indices[bi+1][0] if bi+1<len(month_indices) else len(df)
        for r in range(ds,er):
            rv=df.iloc[r]
            if rv.isnull().all(): break
            dc=str(rv.iloc[1]).strip() if len(rv)>1 else ''
            if dc=='' or dc in ['South','Branch']: continue
            try: float(dc); continue
            except ValueError: pass
            if dc not in KNOWN_DEPOTS: continue
            try:
                all_data.append([month,dc,rv.iloc[2],rv.iloc[3],rv.iloc[5],rv.iloc[6],rv.iloc[7],rv.iloc[8],
                                 rv.iloc[9],rv.iloc[10],rv.iloc[11],rv.iloc[12],rv.iloc[13],rv.iloc[14],
                                 rv.iloc[15],rv.iloc[16],rv.iloc[17],rv.iloc[18],rv.iloc[19],rv.iloc[20]])
            except IndexError: continue
    columns=['Month','Depot','LY_Dedi','LY_Market','LY_IDT','LY_TotalFRT','LY_Vol','LY_RPT',
             'Proj_Dedi','Proj_Market','Proj_IDT','Proj_TotalFRT','Proj_Vol','Proj_RPT',
             'CY_Dedi','CY_Market','CY_IDT','CY_TotalFRT','CY_Vol','CY_RPT']
    df=pd.DataFrame(all_data,columns=columns)
    for col in df.columns:
        if col not in ['Month','Depot']: df[col]=pd.to_numeric(df[col],errors='coerce')
    return df

@st.cache_data
def load_excel(uploaded_file):
    xls=pd.ExcelFile(uploaded_file)
    if 'Sec Summary' not in xls.sheet_names or 'Sec Detailed' not in xls.sheet_names:
        st.error("Required sheets not found."); return None,None
    return (parse_sec_summary(pd.read_excel(xls,sheet_name='Sec Summary',header=None)),
            parse_sec_detailed(pd.read_excel(xls,sheet_name='Sec Detailed',header=None)))

def plot_monthly_bars(df,year_cols,title,tok,series,month_filter=None,depot_filter=None,height=750,
                      single_selection=False):
    attrs=['Dedi','Market','IDT']; cols=[year_cols[a] for a in attrs]
    if df.empty: return None
    if month_filter and month_filter!='All': df=df[df['Month']==month_filter]
    if depot_filter and depot_filter!='All' and 'Depot' in df.columns: df=df[df['Depot']==depot_filter]
    if df.empty: return None
    color_map={'Dedi':series['dedi'],'Market':series['market'],'IDT':series['idt']}
    single_month=(month_filter is not None and month_filter!='All')

    if single_month:
        values=[pd.to_numeric(df[year_cols[a]],errors='coerce').sum() for a in attrs]
        ds=pd.DataFrame({'Attribute':attrs,'Value':values})
        ds=ds[ds['Value'].notna() & (ds['Value']!=0)]
        if ds.empty: return None
        fig=go.Figure()
        add_gradient_bars(fig,x=ds['Attribute'].tolist(),values=ds['Value'].tolist(),
                          base_hex=[color_map[a] for a in ds['Attribute']],tok=tok,width=0.5,text_size=13)
        mv=ds['Value'].max()
        fig.update_layout(barmode='stack',title=dict(text=title,x=0.01,xanchor='left',
            font=dict(color=tok['title'],size=16)),
            margin=dict(t=60,b=30,l=0,r=0),paper_bgcolor=tok['bg'],plot_bgcolor=tok['bg'],
            height=height,showlegend=False,font=dict(color=tok['text']),
            bargap=0.05, bargroupgap=0.0)
        fig.update_yaxes(range=[0,mv*1.18],showticklabels=False,title='',gridcolor=tok['grid'])
        fig.update_xaxes(tickfont=dict(color=tok['axis'],size=13),showgrid=False)
        return fig

    # Multi-month view – if single_selection (depot selected but month All), increase vertical spacing
    if 'Depot' in df.columns and (depot_filter is None or depot_filter=='All'):
        df=df.groupby('Month')[cols].sum().reset_index()
    month_order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    rename_map={year_cols['Dedi']:'Dedi',year_cols['Market']:'Market',year_cols['IDT']:'IDT'}
    df_sub=df[['Month']+cols].rename(columns=rename_map)
    df_sub=df_sub.set_index('Month').reindex(month_order).reset_index()
    for a in ['Dedi','Market','IDT']:
        df_sub[a]=pd.to_numeric(df_sub[a],errors='coerce')
    present=df_sub[['Dedi','Market','IDT']].fillna(0).abs().sum(axis=1)>0
    if not present.any(): return None
    last=present[present].index.max()
    df_sub=df_sub.iloc[:last+1].reset_index(drop=True)
    months_axis=df_sub['Month'].tolist()

    # Adjust spacing based on single_selection
    vert_spacing = 0.18 if single_selection else 0.12
    top_margin = 100 if single_selection else 92

    fig=make_subplots(rows=3,cols=1,shared_xaxes=True,vertical_spacing=vert_spacing,
                      subplot_titles=('<b>Dedi</b>','<b>Market</b>','<b>IDT</b>'))
    for i,attr in enumerate(attrs):
        add_gradient_bars(fig,x=months_axis,values=df_sub[attr].tolist(),
                          base_hex=color_map[attr],tok=tok,row=i+1,col=1,width=0.6,text_size=11)
        vals=pd.to_numeric(df_sub[attr],errors='coerce')
        mv=vals.max(skipna=True); rng=[0,mv*1.2] if (pd.notna(mv) and mv>0) else None
        fig.update_yaxes(range=rng,showticklabels=False,title='',gridcolor=tok['grid'],row=i+1,col=1)
        fig.update_xaxes(categoryorder='array',categoryarray=months_axis,row=i+1,col=1)
    for attr in attrs:
        legend_swatch(fig,attr,color_map[attr],months_axis[0],row=1,col=1)

    fig.update_layout(barmode='stack',title=dict(text=title,x=0.01,xanchor='left',
        font=dict(color=tok['title'],size=16)),
        legend=dict(orientation='h',yanchor='bottom',y=1.015,xanchor='left',x=0.01,
                    traceorder='normal',font=dict(size=12,color=tok['text'])),
        margin=dict(t=top_margin,b=30,l=0,r=0),paper_bgcolor=tok['bg'],plot_bgcolor=tok['bg'],
        height=height,font=dict(color=tok['text']),
        bargap=0.0)
    fig.update_annotations(font=dict(color=tok['text']))
    # Show month labels on all rows
    tick_font_size = 9 if single_selection else 11
    for r in [1,2,3]:
        fig.update_xaxes(tickangle=0, tickmode='array', tickvals=months_axis,
                         tickfont=dict(color=tok['axis'], size=tick_font_size),
                         row=r, col=1, showticklabels=True)
    return fig

def plot_comparison_chart(df, year_option, use_detailed, title, tok, series,
                          month_filter=None, depot_filter=None, height=520,
                          single_selection=False):
    if df.empty: return None
    if month_filter and month_filter!='All': df=df[df['Month']==month_filter]
    if depot_filter and depot_filter!='All' and 'Depot' in df.columns: df=df[df['Depot']==depot_filter]
    if df.empty: return None
    if 'Depot' in df.columns and (depot_filter is None or depot_filter=='All'):
        df=df.groupby('Month').sum().reset_index()
    
    # Always use the three categories: 2025 Actual, 2026 Projection, 2026 Actual
    cols_to_use = {
        '2025 Actual': {
            'Dedi': 'LY_Dedi',
            'Market': 'LY_Market',
            'IDT': 'LY_IDT',
            'TotalFRT': 'LY_TotalFRT',
            'Vol': 'LY_Vol',
            'RPT': 'LY_RPT'
        },
        '2026 Projection': {
            'Dedi': 'Proj_Dedi',
            'Market': 'Proj_Market',
            'IDT': 'Proj_IDT',
            'TotalFRT': 'Proj_TotalFRT',
            'Vol': 'Proj_Vol',
            'RPT': 'Proj_RPT'
        },
        '2026 Actual': {
            'Dedi': 'CY_Dedi',
            'Market': 'CY_Market',
            'IDT': 'CY_IDT',
            'TotalFRT': 'CY_TotalFRT',
            'Vol': 'CY_Vol',
            'RPT': 'CY_RPT'
        }
    }

    all_cols=[]
    for d in cols_to_use.values(): all_cols.extend(list(d.values()))
    sums=df[all_cols].sum()
    types=list(cols_to_use.keys())
    color_for={'2025 Actual':series['ly'],'2026 Projection':series['proj'],
               '2026 Actual':series['cy']}
    disp_attrs=['Dedi','Market','IDT','Total FRT','Vol','RPT']
    attr_key={'Dedi':'Dedi','Market':'Market','IDT':'IDT','Total FRT':'TotalFRT','Vol':'Vol','RPT':'RPT'}

    def getv(tp,akey):
        col=cols_to_use[tp][akey]
        v=sums.get(col,0)
        return float(v) if pd.notna(v) else 0.0

    if sum(abs(getv(tp,attr_key[d])) for tp in types for d in disp_attrs)==0:
        return None

    # ----- SINGLE SELECTION: normalized per metric -----
    if single_selection:
        metrics = disp_attrs
        metric_max = {}
        for m in metrics:
            mx = max([getv(tp, attr_key[m]) for tp in types] + [0.0])
            metric_max[m] = mx if mx > 0 else 1.0

        fig = go.Figure()
        for tp in types:
            real_vals = [getv(tp, attr_key[m]) for m in metrics]
            norm_vals = [real_vals[i] / metric_max[metrics[i]] for i in range(len(metrics))]
            fig.add_trace(go.Bar(
                x=metrics,
                y=norm_vals,
                name=tp,
                marker_color=_shade(color_for[tp], 0.5),
                text=[fmt(v) for v in real_vals],
                textposition='outside',
                textfont=dict(color=tok['text'], size=11, weight='bold'),
                customdata=real_vals,
                cliponaxis=False,
                hovertemplate='%{x}<br>%{customdata:,.2f}<extra></extra>'
            ))

        fig.update_layout(
            barmode='group',
            title=dict(text=title, x=0.01, xanchor='left', font=dict(color=tok['title'], size=16)),
            legend=dict(orientation='h', yanchor='bottom', y=1.015, xanchor='left', x=0.01,
                        traceorder='normal', font=dict(size=12, color=tok['text'])),
            margin=dict(t=100, b=60, l=10, r=10),
            paper_bgcolor=tok['bg'], plot_bgcolor=tok['bg'],
            height=height, font=dict(color=tok['text']),
            bargap=0.05, bargroupgap=0.05
        )
        fig.update_xaxes(tickfont=dict(color=tok['axis'], size=11), showgrid=False)
        fig.update_yaxes(range=[0, 1.15], showticklabels=False, gridcolor=tok['grid'])
        return fig

    # ----- MULTI-MONTH VIEW: bargap = 0.0 -----
    positions=[(1,1),(1,2),(2,1),(2,2),(3,1),(3,2)]
    fig=make_subplots(rows=3,cols=2,subplot_titles=tuple(disp_attrs),
                      vertical_spacing=0.16,horizontal_spacing=0.10)
    type_colors=[color_for[tp] for tp in types]
    for idx,disp in enumerate(disp_attrs):
        r,c=positions[idx]; akey=attr_key[disp]
        vals=[getv(tp,akey) for tp in types]
        add_gradient_bars(fig,x=types,values=vals,base_hex=type_colors,
                          tok=tok,row=r,col=c,width=0.7,text_size=9)
        mv=max(vals+[0]); rng=[0,mv*1.35] if mv>0 else None
        fig.update_yaxes(range=rng,showticklabels=False,title='',gridcolor=tok['grid'],row=r,col=c)

    for tp in types:
        legend_swatch(fig,tp,color_for[tp],types[0],row=1,col=1)

    label_map = {
        '2025 Actual': '2025',
        '2026 Projection': 'Projection',
        '2026 Actual': '2026'
    }
    tick_labels = [label_map.get(t, t) for t in types]
    for r in [1,2,3]:
        for c in [1,2]:
            fig.update_xaxes(
                tickmode='array', tickvals=types, ticktext=tick_labels,
                tickfont=dict(color=tok['axis'], size=9), showticklabels=True, row=r, col=c)

    fig.update_layout(barmode='stack',title=dict(text=title,x=0.01,xanchor='left',
        font=dict(color=tok['title'],size=16)),
        legend=dict(orientation='h', yanchor='top', y=-0.03, xanchor='center', x=0.5,
                    traceorder='normal', font=dict(size=11, color=tok['text'])),
        margin=dict(t=58, b=44, l=0, r=0),
        paper_bgcolor=tok['bg'], plot_bgcolor=tok['bg'],
        height=height, font=dict(color=tok['text']),
        bargap=0.0, bargroupgap=0.0)
    fig.update_annotations(font=dict(color=tok['text']))
    return fig

def main():
    mode=get_theme_mode(); tok=chart_tokens(mode); series=get_series(mode); apply_custom_css(mode)
    st.title("Freight Cost Dashboard"); st.markdown("---")
    uploaded_file=st.file_uploader("Upload Excel file (Cost Template 2026 - Feb'26.xlsx)",type=["xlsx"])
    if uploaded_file is None:
        st.info("Please upload the Excel file to start."); return
    df_summary,df_detailed=load_excel(uploaded_file)
    if df_summary is None or df_detailed is None: st.stop()
    st.session_state['df_summary']=df_summary; st.session_state['df_detailed']=df_detailed
    st.sidebar.header("Filters")
    year_option=st.sidebar.radio("Select Year",('2025','2026'),index=0)
    months=['All']+df_summary['Month'].unique().tolist()
    selected_month=st.sidebar.selectbox("Select Month",months)
    depots=['All']+sorted(df_detailed['Depot'].unique())
    selected_depot=st.sidebar.selectbox("Select Depot",depots)
    use_detailed=(selected_month!='All' or selected_depot!='All')
    if use_detailed:
        df=df_detailed.copy()
        if selected_month!='All': df=df[df['Month']==selected_month]
        if selected_depot!='All': df=df[df['Depot']==selected_depot]
    else:
        df=df_summary.copy()
        if selected_month!='All': df=df[df['Month']==selected_month]
    if year_option=='2025':
        total_frt_col,rpt_col,vol_col='LY_TotalFRT','LY_RPT','LY_Vol'
        year_cols={'Dedi':'LY_Dedi','Market':'LY_Market','IDT':'LY_IDT','TotalFRT':'LY_TotalFRT','Vol':'LY_Vol','RPT':'LY_RPT'}
    else:
        total_frt_col,rpt_col,vol_col='CY_TotalFRT','CY_RPT','CY_Vol'
        year_cols={'Dedi':'CY_Dedi','Market':'CY_Market','IDT':'CY_IDT','TotalFRT':'CY_TotalFRT','Vol':'CY_Vol','RPT':'CY_RPT'}
    if not df.empty:
        total_spent=df[total_frt_col].sum() if total_frt_col in df.columns else 0
        total_rpt=df[rpt_col].sum() if rpt_col in df.columns else 0
        total_vol=df[vol_col].sum() if vol_col in df.columns else 0
    else:
        total_spent=total_rpt=total_vol=0
    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric("Total Spent (Total FRT)",f"₹{fmt(total_spent)}")
    c2.metric("RPT",fmt(total_rpt))
    c3.metric("Volume (Tons)",fmt(total_vol))
    c4.metric("Volume (Cases)","-")
    c5.metric("No. of Vehicles","-")
    st.markdown("---")
    single_selection = (selected_month != 'All' or selected_depot != 'All')
    # Use shorter height for single selection
    chart_height = 420 if single_selection else 750
    col_left,col_right=st.columns(2)
    with col_left:
        title1=f"{year_option} - Monthly Freight Cost Trend [Dedi/Market/IDT]"
        if selected_depot!='All': title1+=f" for {selected_depot}"
        if selected_month!='All': title1+=f" - {selected_month}"
        fig1=plot_monthly_bars(df,year_cols,title1,tok,series,
                               month_filter=selected_month, depot_filter=selected_depot,
                               height=chart_height, single_selection=single_selection)
        if fig1: st.plotly_chart(fig1,use_container_width=True)
        else: st.warning("No data for first chart.")
    with col_right:
        title2="Actual [2025] vs Projection vs Current Year [2026]"
        if selected_depot!='All': title2+=f" for {selected_depot}"
        if selected_month!='All': title2+=f" - {selected_month}"
        cmp_h = chart_height
        fig2=plot_comparison_chart(df,year_option,use_detailed,title2,tok,series,
                                   month_filter=selected_month, depot_filter=selected_depot,
                                   height=cmp_h, single_selection=single_selection)
        if fig2: st.plotly_chart(fig2,use_container_width=True)
        else: st.warning("No data for comparison chart.")
    st.markdown("---")
    st.subheader("Vehicle Distribution (Mock Data)")
    mock_data={'Transporter A':15,'Transporter B':22,'Transporter C':10,'Transporter D':8}
    fig_pie=px.pie(values=list(mock_data.values()),names=list(mock_data.keys()),
        title="Vehicle Count by Transporter",
        color_discrete_sequence=[series['dedi'],series['market'],series['idt'],series['cy']])
    fig_pie.update_traces(textfont=dict(color=tok['text']))
    fig_pie.update_layout(legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='center',x=0.5,
        font=dict(size=9,color=tok['text'])),margin=dict(t=40,b=10),
        paper_bgcolor=tok['bg'],plot_bgcolor=tok['bg'],font=dict(color=tok['text']),
        title=dict(font=dict(color=tok['title'],size=16)))
    st.plotly_chart(fig_pie,use_container_width=True)

if __name__ == "__main__":
    main()