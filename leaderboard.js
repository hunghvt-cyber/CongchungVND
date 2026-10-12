/* Public aggregate scores; never request or publish a history capability. */
(() => {
  const root = document.querySelector('#sharedLeaderboard');
  if (!root) return;
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const pageSize = 100;
  let config, offset = 0, generation = 0;
  root.innerHTML = `<div class="leaderboard-heading"><div><p class="eyebrow">Cùng nhau tiến bộ</p><h2>Bảng xếp hạng chung</h2></div><button id="refreshLeaderboard" class="secondary-button">Làm mới</button></div><p>Điểm trung bình các bài thi thử đã lưu, quy đổi về thang 10. Cần ít nhất <strong>3 bài thi</strong> để được xếp hạng; bằng điểm thì ưu tiên người có nhiều lượt thi hơn.</p><p class="name-note">Mỗi số điện thoại là một lịch sử riêng, kể cả khi trùng tên. Khi đổi thiết bị, nhập lại cùng số điện thoại để tiếp tục thành tích. Đề có độ khó và phạm vi khác nhau; bảng dùng để động viên tự luyện.</p><p id="leaderboardStatus" role="status"></p><div id="leaderboardContent"></div><div class="leaderboard-pagination"><button id="leaderboardPrevious" class="secondary-button hidden">← Trang trước</button><button id="leaderboardNext" class="secondary-button hidden">Trang tiếp →</button></div>`;
  const status = root.querySelector('#leaderboardStatus');
  const content = root.querySelector('#leaderboardContent');
  const refreshButton = root.querySelector('#refreshLeaderboard');
  const previous = root.querySelector('#leaderboardPrevious');
  const next = root.querySelector('#leaderboardNext');
  function markup(rows, start) {
    return `<div class="leaderboard-table-wrap"><table class="leaderboard-table"><caption>Xếp hạng ${start + 1}–${start + rows.length}</caption><thead><tr><th scope="col">Hạng</th><th scope="col">Người thi</th><th scope="col">Lượt thi</th><th scope="col">Điểm TB</th><th scope="col">Cao nhất</th></tr></thead><tbody>${rows.map((row, i) => `<tr><td>${start + i + 1}</td><th scope="row">${esc(row.learner_name)}</th><td>${Number(row.attempt_count)}</td><td><strong>${Number(row.average_score).toFixed(2)}</strong></td><td>${Number(row.best_score).toFixed(2)}</td></tr>`).join('')}</tbody></table></div>`;
  }
  async function load(start = 0) {
    const token = ++generation;
    status.textContent = 'Đang tải bảng xếp hạng…';
    [refreshButton, previous, next].forEach(b => b.disabled = true);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    try {
      if (!config) {
        const response = await fetch('./data/feedback-config.json', {cache:'no-cache', signal:controller.signal});
        if (!response.ok) throw Error('config');
        const loaded = await response.json();
        if (!/^https:\/\/[a-z0-9]+\.supabase\.co$/.test(loaded.url) || !loaded.publishableKey?.startsWith('sb_publishable_')) throw Error('config');
        config = loaded;
      }
      const url = `${config.url}/rest/v1/exam_leaderboard?select=learner_name,attempt_count,average_score,best_score&order=average_score.desc,attempt_count.desc,id.asc&limit=${pageSize + 1}&offset=${start}`;
      const response = await fetch(url, {headers:{apikey:config.publishableKey}, cache:'no-store', signal:controller.signal});
      if (!response.ok) throw Error('network');
      const rows = await response.json();
      if (!Array.isArray(rows) || rows.some(r => typeof r.learner_name !== 'string' || !Number.isInteger(Number(r.attempt_count)) || Number(r.attempt_count) < 3 || !Number.isFinite(Number(r.average_score)) || Number(r.average_score) < 0 || Number(r.average_score) > 10 || !Number.isFinite(Number(r.best_score)) || Number(r.best_score) < 0 || Number(r.best_score) > 10)) throw Error('data');
      if (token !== generation) return;
      if (!rows.length && start > 0) { await load(0); return; }
      offset = start;
      content.innerHTML = rows.length ? markup(rows.slice(0,pageSize), start) : '<p>Chưa có người thi đủ 3 bài đã lưu. Hoàn thành thêm bài thi thử để tham gia bảng xếp hạng.</p>';
      previous.classList.toggle('hidden', start === 0);
      next.classList.toggle('hidden', rows.length <= pageSize);
      status.textContent = `Cập nhật lúc ${new Date().toLocaleTimeString('vi-VN')}.`;
    } catch {
      if (token === generation) status.textContent = 'Chưa tải được bảng xếp hạng. Bấm Làm mới để thử lại. Dữ liệu đang hiển thị, nếu có, là lần tải trước.';
    } finally {
      clearTimeout(timeout);
      if (token === generation) [refreshButton, previous, next].forEach(b => b.disabled = false);
    }
  }
  refreshButton.onclick = () => load(0);
  previous.onclick = () => load(Math.max(0, offset - pageSize));
  next.onclick = () => load(offset + pageSize);
  window.ExamLeaderboard = {refresh:() => load(0), markup};
  load(0);
})();
