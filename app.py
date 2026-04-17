import streamlit as st
import groq
import base64
import io
from PIL import Image, ImageOps
import fitz  # PyMuPDF
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()  # Adds HEIC/HEIF support to Pillow
except ImportError:
    pass  # Graceful fallback if not installed

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="HandScript AI · Digit Analyzer",
    page_icon="🔢",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', system-ui, sans-serif; }

.stApp { background: #F7F8FC; }

header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }

.block-container {
    max-width: 740px !important;
    padding-top: 2rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
    padding-bottom: 3rem !important;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 60%, #A78BFA 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.75rem;
    box-shadow: 0 8px 32px rgba(99,102,241,0.18);
}
.hero h1 {
    color: #fff;
    font-size: clamp(1.6rem, 4vw, 2.3rem);
    font-weight: 700;
    margin: 0 0 0.35rem;
    letter-spacing: -0.5px;
}
.hero p {
    color: rgba(255,255,255,0.82);
    font-size: clamp(0.83rem, 2.4vw, 0.97rem);
    margin: 0;
}

/* Cards */
.card {
    background: #fff;
    border-radius: 16px;
    padding: 1.6rem 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
    border: 1px solid #EBEBF0;
}
.card-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #6366F1;
    margin-bottom: 1rem;
}

/* Uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #D1D5DB !important;
    border-radius: 14px !important;
    background: #FAFAFA !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover { border-color: #6366F1 !important; }

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.72rem 1.5rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover  { opacity: 0.9 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* Download button — secondary style */
[data-testid="stDownloadButton"] > button {
    background: #F5F3FF !important;
    color: #4338CA !important;
    border: 1.5px solid #C7D2FE !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    width: 100%;
    transition: background 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover { background: #EEF2FF !important; }

/* Digit frequency table */
.freq-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}
.freq-table th {
    background: #EEF2FF;
    color: #3730A3;
    font-weight: 600;
    padding: 0.55rem 1rem;
    text-align: left;
    border-radius: 8px 8px 0 0;
}
.freq-table td {
    padding: 0.5rem 1rem;
    border-bottom: 1px solid #F0F0F5;
    color: #374151;
}
.freq-table tr:last-child td { border-bottom: none; }
.freq-table tr:hover td { background: #FAFAFF; }

/* Bar inside table */
.bar-wrap { background: #EEF2FF; border-radius: 999px; height: 8px; min-width: 60px; }
.bar-fill  { background: linear-gradient(90deg, #6366F1, #8B5CF6); border-radius: 999px; height: 8px; }

/* Transcription box */
.transcript-box {
    background: #F9FAFB;
    border: 1.5px solid #E5E7EB;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    font-family: 'Inter', monospace;
    font-size: 1.05rem;
    letter-spacing: 0.04em;
    line-height: 1.9;
    color: #1F2937;
    word-break: break-word;
}

/* Info / error strips */
.info-strip {
    background: #F0FDF4; border: 1px solid #BBF7D0;
    border-radius: 10px; padding: 0.65rem 1rem;
    font-size: 0.82rem; color: #166534; margin-bottom: 0.9rem;
}
.error-strip {
    background: #FFF1F2; border: 1px solid #FECDD3;
    border-radius: 10px; padding: 0.65rem 1rem;
    font-size: 0.82rem; color: #9F1239; margin-bottom: 0.9rem;
}

/* Metric pills */
.pill-row { display: flex; flex-wrap: wrap; gap: 0.55rem; margin-top: 0.75rem; }
.pill {
    background: #EEF2FF; color: #4338CA;
    border-radius: 999px; padding: 0.28rem 0.8rem;
    font-size: 0.76rem; font-weight: 500;
}

/* Spinner */
.stSpinner > div { border-top-color: #6366F1 !important; }

hr { border: none; border-top: 1px solid #EBEBF0; margin: 1.5rem 0; }

[data-testid="stImage"] img {
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
}

@media (max-width: 600px) {
    .hero { padding: 1.75rem 1.1rem; }
    .card { padding: 1.2rem 1rem; }
    .block-container { padding-left: 0.7rem !important; padding-right: 0.7rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def get_client() -> groq.Groq:
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key or api_key == "your_groq_api_key_here":
        st.markdown(
            '<div class="error-strip">⚠️ <strong>API key missing.</strong> '
            'Open <code>.streamlit/secrets.toml</code> and paste your Groq key.</div>',
            unsafe_allow_html=True,
        )
        st.stop()
    return groq.Groq(api_key=api_key)


def to_base64(image: Image.Image) -> str:
    buf = io.BytesIO()
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


def downscale(image: Image.Image, max_px: int = 1280) -> Image.Image:
    w, h = image.size
    if max(w, h) > max_px:
        r = max_px / max(w, h)
        image = image.resize((int(w * r), int(h * r)), Image.LANCZOS)
    return image


def pdf_to_images(pdf_bytes: bytes, dpi: int = 180) -> list:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    for page in doc:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pages.append(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    doc.close()
    return pages


def open_image(file) -> Image.Image:
    """Robustly open any image file from any source (phone, WhatsApp, HEIC, etc.)."""
    img = Image.open(file)
    # Fix EXIF rotation — phone/camera images store rotation as metadata only
    img = ImageOps.exif_transpose(img)
    # Normalise color mode → RGB
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")
    return img


SYSTEM_PROMPT = """You are an expert handwriting analyst specialising in handwritten digits and numbers.

Look at the handwriting sample and list every number you can read, row by row, exactly as written.
Return ONLY a plain text list — no JSON, no explanation, no extra commentary.
Preserve the row structure using newlines. Separate individual numbers on the same row with a space.
If a digit is ambiguous, include your best guess.
"""


def analyze(client: groq.Groq, image: Image.Image) -> str:
    img_b64 = to_base64(downscale(image))
    resp = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                {"type": "text", "text": "List all the numbers you can see in this handwriting sample and ignore the duplicates."},
            ]},
        ],
        temperature=0.2,
        max_tokens=800,
    )
    return resp.choices[0].message.content.strip()


# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <h1>🔢 HandScript AI</h1>
    <p>Upload a handwritten digit sample — identify which numbers are in it</p>
</div>
""", unsafe_allow_html=True)

client = get_client()

# ── Upload ──────────────────────────────────
# Session state for resetting uploader
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

st.markdown(
    '<p style="font-size:0.78rem;font-weight:600;letter-spacing:0.09em;text-transform:uppercase;'
    'color:#6366F1;margin-bottom:0.5rem;">📁 Upload Sample</p>'
    '<p style="font-size:0.84rem;color:#6B7280;margin-bottom:0.5rem;">'
    'Accepts any image format (JPG, PNG, HEIC, WEBP, BMP, TIFF, …) or PDF — max 10 MB</p>',
    unsafe_allow_html=True,
)
uploaded = st.file_uploader(
    "Upload",
    type=None,   # Accept every file type
    key=f"uploader_{st.session_state['uploader_key']}",
    label_visibility="collapsed",
)

# ── Clear button ──────────────────────────────
if uploaded or "result" in st.session_state:
    if st.button("✕ Clear", use_container_width=False):
        st.session_state["uploader_key"] += 1
        st.session_state.pop("result", None)
        st.rerun()

# ── Process file ────────────────────────────
raw_image = None
is_pdf = False
pdf_pages = []
selected_page = 0

if uploaded:
    is_pdf = uploaded.type == "application/pdf"

    if is_pdf:
        with st.spinner("Rendering PDF…"):
            pdf_pages = pdf_to_images(uploaded.read())
        num_pages = len(pdf_pages)

        st.markdown(
            f'<p style="font-size:0.78rem;font-weight:600;letter-spacing:0.09em;text-transform:uppercase;'
            f'color:#6366F1;margin:1.2rem 0 0.5rem;">📄 PDF — {num_pages} page{"s" if num_pages > 1 else ""}</p>',
            unsafe_allow_html=True,
        )
        if num_pages > 1:
            cols = st.columns(min(num_pages, 8))
            for i, col in enumerate(cols[:num_pages]):
                col.image(downscale(pdf_pages[i].copy(), 200), caption=f"p.{i+1}", use_container_width=True)
            selected_page = st.selectbox(
                "Select page",
                range(num_pages),
                format_func=lambda x: f"Page {x+1}",
                label_visibility="collapsed",
            )
        else:
            st.info("📃 Single-page PDF detected.")
        raw_image = pdf_pages[selected_page]
    else:
        try:
            raw_image = open_image(uploaded)
        except Exception:
            st.error("⚠️ Could not read this file. Please upload a valid image (JPG, PNG, HEIC, WEBP, BMP, TIFF) or PDF.")
            raw_image = None

# ── Preview ─────────────────────────────────
if raw_image:
    display = downscale(raw_image.copy(), 900)
    w, h = raw_image.size
    page_tag = f" · p.{selected_page+1}/{len(pdf_pages)}" if is_pdf and len(pdf_pages) > 1 else ""
    file_tag = f"PDF{page_tag}" if is_pdf else uploaded.type.split("/")[-1].upper()

    st.markdown(
        f'<p style="font-size:0.78rem;font-weight:600;letter-spacing:0.09em;text-transform:uppercase;'
        f'color:#6366F1;margin:1.2rem 0 0.5rem;">🖼 Preview{page_tag}</p>',
        unsafe_allow_html=True,
    )
    st.image(display, use_container_width=True)
    st.markdown(
        f'<div class="pill-row" style="margin-bottom:1rem;">'
        f'<span class="pill">📐 {w}×{h}px</span>'
        f'<span class="pill">📄 {file_tag}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Analyze button ───────────────────────
    if st.button("🔍 Analyze Digits", use_container_width=True):
        with st.spinner("Analyzing handwritten digits…"):
            try:
                result = analyze(client, raw_image)
                st.session_state["result"] = result
            except Exception as e:
                st.error(f"❌ **Error:** {e}")

# ── Results ──────────────────────────────────
if "result" in st.session_state:
    st.divider()
    st.markdown(
        '<p style="font-size:0.78rem;font-weight:600;letter-spacing:0.09em;text-transform:uppercase;'
        'color:#6366F1;margin-bottom:0.5rem;">🔢 Numbers Found</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="transcript-box">{st.session_state["result"]}</div>',
        unsafe_allow_html=True,
    )

# ── Empty state ──────────────────────────────
if not uploaded:
    st.markdown("""
    <div style="text-align:center;padding:2.5rem 1rem;color:#9CA3AF;">
        <div style="font-size:3rem;margin-bottom:0.75rem;">🔢</div>
        <p style="font-size:0.9rem;margin:0;">
            Upload a handwritten digit sample above.<br>
            Works with answer sheets, math homework, and any number-heavy pages.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────
st.markdown("""
<hr>
<div style="text-align:center;font-size:0.74rem;color:#9CA3AF;padding-bottom:1rem;">
    Powered by <strong style="color:#6366F1;">Groq</strong> ·
    <span style="font-family:monospace;">llama-4-scout-17b</span> · HandScript AI
</div>
""", unsafe_allow_html=True)
