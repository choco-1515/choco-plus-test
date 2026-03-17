:root {
    --bg-color: #121212;
    --text-color: #fff;
    --accent-color: #fa9d5a;
    --header-bg: #1e1e1e;
    --card-bg: #2a2a2a;
    --hover-bg: #383838;
}

body {
    font-family: "Roboto", "Arial", sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    padding-top: 60px;
}

header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background: var(--header-bg);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    box-sizing: border-box;
    z-index: 1000;
    border-bottom: 1px solid #333;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--accent-color);
    text-decoration: none;
    display: flex;
    align-items: center;
}

.logo span {
    color: #fff;
    margin-left: 2px;
}

.search-container {
    flex: 1;
    max-width: 600px;
    margin: 0 20px;
    position: relative;
}

.search-form {
    display: flex;
    width: 100%;
    background: #2a2a2a;
    border: 1px solid #444;
    border-radius: 40px;
    overflow: hidden;
}

.search-form input {
    flex: 1;
    background: transparent;
    border: none;
    color: #fff;
    padding: 10px 20px;
    outline: none;
    font-size: 1rem;
}

.search-form button {
    background: #444;
    border: none;
    color: #fff;
    padding: 0 20px;
    cursor: pointer;
}

.search-form button:hover {
    background: #555;
}

main {
    padding: 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.video-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 20px;
}

.video-card {
    background: var(--card-bg);
    border-radius: 12px;
    overflow: hidden;
    text-decoration: none;
    color: inherit;
    transition: transform 0.2s, background 0.2s;
}

.video-card:hover {
    background: var(--hover-bg);
    transform: translateY(-5px);
}

.video-card .thumbnail-container {
    width: 100%;
    aspect-ratio: 16/9;
    overflow: hidden;
    background: #000;
    position: relative;
}

.video-card img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.video-duration {
    position: absolute;
    bottom: 8px;
    right: 8px;
    background: rgba(0, 0, 0, 0.8);
    color: #fff;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
}

.video-info {
    padding: 12px;
}

.video-info h3 {
    margin: 0 0 8px 0;
    font-size: 1rem;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.video-info p {
    margin: 0;
    font-size: 0.85rem;
    color: #aaa;
}

.video-meta {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-top: 8px;
    font-size: 0.75rem;
    color: #888;
}

.view-count, .published-date {
    display: block;
    word-break: break-word;
}

.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #1e1e1e;
    display: flex;
    justify-content: space-around;
    padding: 10px 0;
    border-top: 1px solid #333;
    z-index: 1000;
}

.bottom-nav a {
    color: #aaa;
    text-decoration: none;
    font-size: 0.9rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.bottom-nav a.active {
    color: var(--accent-color);
}

.pagination {
    display: flex;
    justify-content: center;
    padding: 40px 0 80px 0;
}

.next-btn {
    padding: 12px 40px;
    background: #444;
    color: #fff;
    text-decoration: none;
    border-radius: 30px;
    font-weight: bold;
}

@media (max-width: 600px) {
    header {
        padding: 0 10px;
    }
    .search-container {
        margin: 0 10px;
    }
    .logo span {
        display: none;
    }
}

/* ============================================================
   watch ページ専用スタイル
   ============================================================ */

.watch-container {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 20px;
    max-width: 1200px;
    margin: 20px auto;
    padding: 0 15px;
}

.video-section {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.player-wrapper {
    position: relative;
}

.stream-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    flex-wrap: wrap;
}

.stream-btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background: #333;
    color: #fff;
    cursor: pointer;
    font-weight: 600;
    font-size: 14px;
    transition: all 0.2s;
}

.stream-btn.active {
    background: #ff6b00;
    color: white;
}

.stream-btn:hover {
    background: #444;
}

.stream-btn.active:hover {
    background: #ff8533;
}

.quality-selector {
    display: none;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 10px;
    background: #1a1a1a;
    border-radius: 8px;
    padding: 12px;
}

.quality-selector.show {
    display: flex;
}

.quality-tabs {
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
}

.quality-tab {
    padding: 6px 14px;
    border: none;
    border-radius: 4px;
    background: #2a2a2a;
    color: #aaa;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.2s;
}

.quality-tab.active {
    background: #ff6b00;
    color: white;
}

.quality-tab:hover:not(.active) {
    background: #383838;
    color: #fff;
}

.quality-options {
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
}

#btn-show-all-streams,
#btn-ytdlp-show-all-streams {
    background: #2a2a2a;
    color: #aaa;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
    margin-left: auto;
    align-self: flex-end;
    flex-shrink: 0;
}
#btn-show-all-streams:hover,
#btn-ytdlp-show-all-streams:hover { background: #383838; color: #fff; }

.quality-option-wrap {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    border: 1px solid #3a3a3a;
    border-radius: 5px;
    padding: 2px 4px;
}

.quality-check {
    cursor: pointer;
    font-size: 15px;
    line-height: 1;
    user-select: none;
    padding: 2px 3px;
    border-radius: 3px;
    transition: background 0.15s;
}
.quality-check:hover { background: #383838; }

.quality-option {
    padding: 5px 12px;
    border: 1px solid #444;
    border-radius: 4px;
    background: #222;
    color: #aaa;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.2s;
}

.quality-option:hover {
    border-color: #ff6b00;
    color: #fff;
}

.quality-option.selected {
    background: #ff6b00;
    color: white;
    border-color: #ff6b00;
}

#btn-inv-log {
    margin-left: 6px;
    background: #2a2a2a;
    color: #aaa;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
}
#btn-inv-log:hover { background: #383838; color: #fff; }
#btn-inv-log.log-open { background: #333; color: #fff; border-color: #aaa; }

#inv-log-overlay {
    display: none;
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.88);
    z-index: 50;
    border-radius: 12px;
    padding: 14px 16px;
    overflow-y: auto;
    font-family: monospace;
    font-size: 12px;
    line-height: 1.6;
    color: #ccc;
}
#inv-log-overlay.visible { display: block; }
#inv-log-overlay .log-line { border-bottom: 1px solid #222; padding: 2px 0; word-break: break-all; }
#inv-log-overlay .log-warn { color: #f90; }
#inv-log-overlay .log-err  { color: #f55; }

#btn-ytdlp-log {
    margin-left: 6px;
    background: #2a2a2a;
    color: #aaa;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
}
#btn-ytdlp-log:hover { background: #383838; color: #fff; }
#btn-ytdlp-log.log-open { background: #333; color: #fff; border-color: #aaa; }

#ytdlp-log-overlay {
    display: none;
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.88);
    z-index: 50;
    border-radius: 12px;
    padding: 14px 16px;
    overflow-y: auto;
    font-family: monospace;
    font-size: 12px;
    line-height: 1.6;
    color: #ccc;
}
#ytdlp-log-overlay.visible { display: block; }
#ytdlp-log-overlay .log-line { border-bottom: 1px solid #222; padding: 2px 0; word-break: break-all; }
#ytdlp-log-overlay .log-warn { color: #f90; }
#ytdlp-log-overlay .log-err  { color: #f55; }

.player-container {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    background: #000;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.player-container video,
.player-container audio {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.player-error {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: #000;
}

.error-message-box {
    background: rgba(255, 68, 68, 0.95);
    color: white;
    padding: 30px;
    border-radius: 8px;
    text-align: center;
    max-width: 400px;
}

.error-message {
    font-size: 16px;
    margin-bottom: 20px;
    font-weight: 500;
}

.reload-button {
    background: white;
    color: #ff4444;
    border: none;
    padding: 10px 30px;
    border-radius: 5px;
    font-weight: 600;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.2s;
}

.reload-button:hover {
    background: #f0f0f0;
}

.loading-spinner {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.spinner {
    display: inline-block;
    width: 40px;
    height: 40px;
    border: 4px solid #333;
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* ---- 動画再生について（折りたたみ枠） ---- */
.playback-info-box {
    background: #1a1a1a;
    border-radius: 8px;
    overflow: hidden;
}

.playback-info-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    cursor: pointer;
    user-select: none;
    transition: background 0.15s;
}

.playback-info-header:hover {
    background: #222;
}

.playback-info-title {
    font-size: 14px;
    font-weight: 600;
    color: #ccc;
}

.playback-info-toggle {
    background: #2a2a2a;
    border: 1px solid #444;
    border-radius: 4px;
    color: #aaa;
    font-size: 18px;
    line-height: 1;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    flex-shrink: 0;
}

.playback-info-toggle:hover {
    background: #383838;
    color: #fff;
}

.playback-info-body {
    display: none;
    padding: 0 16px 14px;
    font-size: 13px;
    color: #aaa;
    border-top: 1px solid #2a2a2a;
}

.playback-info-body.open {
    display: block;
}

/* ---- 動画タイトル・チャンネル（カードなし、YouTube風） ---- */
.video-metadata {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.video-title {
    font-size: 18px;
    font-weight: 700;
    color: #fff;
    line-height: 1.4;
    margin: 0 0 8px 0;
}

.channel-info {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 0;
    border-top: 1px solid #2a2a2a;
    border-bottom: 1px solid #2a2a2a;
}

.channel-link {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: inherit;
    flex: 1;
    min-width: 0;
    border-radius: 8px;
    padding: 2px 6px 2px 2px;
    margin: -2px -6px -2px -2px;
    transition: background 0.15s;
}
.channel-link:hover {
    background: rgba(255,255,255,0.07);
}

.channel-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #333;
    flex-shrink: 0;
    object-fit: cover;
}

.channel-details { flex: 1; min-width: 0; }

.channel-name {
    font-weight: 600;
    color: #fff;
    font-size: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.channel-subs {
    font-size: 13px;
    color: #aaa;
    margin-top: 1px;
}

/* ---- 高評価・低評価バー ---- */
.like-dislike-bar {
    display: flex;
    align-items: center;
    background: #272727;
    border-radius: 999px;
    height: 36px;
    flex-shrink: 0;
    overflow: hidden;
    transition: background 0.15s;
}

.like-dislike-bar:hover {
    background: #3f3f3f;
}

.like-btn, .dislike-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0 14px;
    height: 100%;
    border: none;
    background: transparent;
    color: #fff;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
}

.like-btn {
    border-right: 1px solid rgba(255,255,255,0.15);
    padding-right: 12px;
}

.dislike-btn {
    padding-left: 12px;
}

.like-btn svg, .dislike-btn svg {
    width: 24px;
    height: 24px;
    fill: currentColor;
    flex-shrink: 0;
}

.reload-stream-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #272727;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    border: none;
    cursor: pointer;
    color: #fff;
    flex-shrink: 0;
    transition: background 0.15s;
}
.reload-stream-btn:hover {
    background: #3f3f3f;
}
.reload-stream-btn svg {
    width: 24px;
    height: 24px;
    fill: currentColor;
}

/* ---- コピートースト ---- */
#copy-toast {
    position: fixed;
    bottom: 32px;
    left: 50%;
    transform: translateX(-50%) translateY(16px);
    background: #e8e8e8;
    color: #111;
    padding: 10px 20px;
    border-radius: 24px;
    font-size: 14px;
    font-weight: 500;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.2s, transform 0.2s;
    z-index: 9999;
    white-space: nowrap;
}
#copy-toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

/* ---- 動画メタデータ枠（準備中） ---- */
.video-desc-box {
    background: #1a1a1a;
    border-radius: 8px;
    padding: 14px 16px;
    margin-top: 12px;
    font-size: 13px;
    color: #aaa;
    cursor: pointer;
    transition: background 0.15s;
}
.video-desc-box:hover { background: #222; }
.video-desc-label {
    font-size: 12px;
    font-weight: 600;
    color: #888;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}

.comments-section {
    background: #1a1a1a;
    padding: 20px;
    border-radius: 8px;
    grid-column: 1;
    margin-top: 10px;
}

.comments-title {
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 15px;
    color: #fff;
}

.comment-placeholder {
    color: #aaa;
    text-align: center;
    padding: 30px;
    font-size: 14px;
}

.related-videos {
    background: #1a1a1a;
    border-radius: 8px;
    overflow: hidden;
}

.related-title {
    padding: 15px;
    font-weight: 600;
    border-bottom: 1px solid #333;
    color: #fff;
    font-size: 14px;
}

@media (max-width: 900px) {
    .watch-container { grid-template-columns: 1fr; }
    .video-info { flex-direction: column; gap: 10px; }
}
