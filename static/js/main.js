let rawEntries = [];
let currentEntries = [];
let currentViewedId = null;
let searchTimeout = null;
let activeTalentCategory = '';

document.addEventListener('DOMContentLoaded', () => {
    loadEntries();
});

async function loadEntries() {
    const q = document.getElementById('searchInput')?.value.trim() || '';
    const sinf = document.getElementById('filterSinf')?.value || '';
    const til = document.getElementById('filterTil')?.value || '';
    const kasb = document.getElementById('filterKasb')?.value.trim() || '';

    const params = new URLSearchParams();
    if (q) params.append('q', q);
    if (sinf) params.append('sinf', sinf);
    if (til) params.append('til', til);
    if (kasb) params.append('kasb', kasb);

    try {
        const res = await fetch(`/api/entries?${params.toString()}`);
        if (res.status === 401) {
            window.location.href = '/admin/login?next=/admin';
            return;
        }
        const result = await res.json();
        if (result.status === 'success') {
            rawEntries = result.data;
            applyTalentFilterAndRender();
        } else {
            console.error("API xatosi:", result);
            showToast(result.message || "Xatolik yuz berdi", "error");
        }
    } catch (err) {
        console.error("Ma'lumot yuklashda xatolik:", err);
        showToast("Ma'lumotlarni yuklab bo'lmadi", "error");
    }
}

async function syncGoogleSheet() {
    const btn = document.getElementById('btnSyncSheet');
    const origHtml = btn ? btn.innerHTML : '';
    if (btn) {
        btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin text-emerald-600"></i> <span>Sinxronlanmoqda...</span>';
        btn.disabled = true;
        lucide.createIcons();
    }
    try {
        const res = await fetch('/api/sync-google-sheet', { method: 'POST' });
        const data = await res.json();
        if (data.status === 'success') {
            showToast(data.message, 'success');
            await loadEntries();
        } else {
            showToast(data.message || 'Sinxronlashda xatolik', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast("Google Sheet bilan bog'lanishda xatolik", 'error');
    } finally {
        if (btn) {
            btn.innerHTML = origHtml;
            btn.disabled = false;
            lucide.createIcons();
        }
    }
}

function onClassFilterChange() {
    const sinf = document.getElementById('filterSinf')?.value;
    const btnText = document.getElementById('btnClassExportText');
    const btn = document.getElementById('btnClassExport');

    if (sinf) {
        if (btnText) btnText.textContent = `${sinf} Excel yuklash`;
        if (btn) {
            btn.className = "px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs sm:text-sm rounded-xl shadow-md shadow-emerald-200 flex items-center space-x-1.5 transition-all";
        }
    } else {
        if (btnText) btnText.textContent = "Excel yuklash";
        if (btn) {
            btn.className = "px-3.5 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 font-semibold text-xs sm:text-sm rounded-xl flex items-center space-x-1.5 transition-all";
        }
    }

    loadEntries();
}

function exportFilteredExcel() {
    const sinf = document.getElementById('filterSinf')?.value || '';
    if (sinf) {
        window.location.href = `/export/excel?sinf=${encodeURIComponent(sinf)}`;
    } else {
        window.location.href = '/export/excel';
    }
}

function setTalentFilter(category) {
    activeTalentCategory = category;

    const tabs = {
        '': 'tabTalentAll',
        'it': 'tabTalentIT',
        'tibbiyot': 'tabTalentMed',
        'sport': 'tabTalentSport',
        'biznes': 'tabTalentBiz',
        'sanat': 'tabTalentArt',
        'togaraksiz': 'tabTalentNoClub'
    };

    Object.entries(tabs).forEach(([cat, id]) => {
        const el = document.getElementById(id);
        if (!el) return;
        if (cat === category) {
            el.className = cat === 'togaraksiz'
                ? "px-3 py-1.5 rounded-xl font-bold bg-rose-600 text-white shadow-sm transition-all whitespace-nowrap"
                : "px-3 py-1.5 rounded-xl font-bold bg-emerald-600 text-white shadow-sm transition-all whitespace-nowrap";
        } else {
            el.className = cat === 'togaraksiz'
                ? "px-3 py-1.5 rounded-xl font-semibold bg-rose-50 text-rose-700 hover:bg-rose-100 transition-all whitespace-nowrap border border-rose-200"
                : "px-3 py-1.5 rounded-xl font-semibold bg-gray-100 text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 transition-all whitespace-nowrap";
        }
    });

    applyTalentFilterAndRender();
}

function applyTalentFilterAndRender() {
    if (!activeTalentCategory) {
        currentEntries = [...rawEntries];
    } else {
        currentEntries = rawEntries.filter(item => {
            if (activeTalentCategory === 'togaraksiz') {
                const t = (item.togaraklar || '').toLowerCase();
                return !t || t.includes('bormayman') || t.includes('yoq') || t.includes("yo'q");
            }
            const str = `${item.iqtidor} ${item.kasb} ${item.yangi_togaraklar} ${item.fanlar} ${item.togaraklar}`.toLowerCase();
            if (activeTalentCategory === 'it') {
                return str.includes('it') || str.includes('dastur') || str.includes('robot') || str.includes('veb') || str.includes('informatika');
            } else if (activeTalentCategory === 'tibbiyot') {
                return str.includes('shifokor') || str.includes('tibbiyot') || str.includes('vrach') || str.includes('biologiya') || str.includes('kimyo') || str.includes('jarroh') || str.includes('stomatolog');
            } else if (activeTalentCategory === 'sport') {
                return str.includes('sport') || str.includes('harbiy') || str.includes('futbol') || str.includes('shaxmat') || str.includes('basketbol') || str.includes('jismoniy');
            } else if (activeTalentCategory === 'biznes') {
                return str.includes('biznes') || str.includes('tadbirkor') || str.includes('startap') || str.includes('moliya') || str.includes('iqtisod') || str.includes('bank') || str.includes('yetakchilik');
            } else if (activeTalentCategory === 'sanat') {
                return str.includes("san'at") || str.includes('sanat') || str.includes('rasm') || str.includes('musiqa') || str.includes('dizayn') || str.includes('raqs') || str.includes('ijod');
            }
            return true;
        });
    }

    renderTable(currentEntries);
}

function renderTable(entries) {
    const tbody = document.getElementById('tableBody');
    const emptyState = document.getElementById('emptyState');
    const tableFooter = document.getElementById('tableFooter');
    const badgeCount = document.getElementById('badgeCount');
    const displayedCount = document.getElementById('displayedCount');

    if (badgeCount) badgeCount.textContent = `${entries.length} ta yozuv`;
    if (displayedCount) displayedCount.textContent = entries.length;

    if (!entries || entries.length === 0) {
        tbody.innerHTML = '';
        emptyState.classList.remove('hidden');
        emptyState.classList.add('flex');
        if (tableFooter) tableFooter.classList.add('hidden');
        return;
    }

    emptyState.classList.add('hidden');
    emptyState.classList.remove('flex');
    if (tableFooter) tableFooter.classList.remove('hidden');

    let html = '';
    entries.forEach((item, index) => {
        const tilBadge = item.til === 'Русский' 
            ? '<span class="px-2 py-0.5 rounded-lg text-[11px] font-bold bg-blue-50 text-blue-700 border border-blue-200">Русский</span>'
            : '<span class="px-2 py-0.5 rounded-lg text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">O&#39;zbek</span>';

        const sinfBadge = `<span class="px-2.5 py-0.5 rounded-lg text-[11px] font-extrabold bg-gray-100 text-gray-800 border border-gray-200">${escapeHtml(item.sinf)}</span>`;

        html += `
        <tr class="sheet-row border-b border-gray-200 transition-colors bg-white">
            <td class="px-2 py-2.5 text-center text-gray-400 font-mono text-[11px] bg-gray-50 select-none">${index + 1}</td>
            <td class="px-3 py-2.5 text-gray-600 font-mono text-[11px]">${escapeHtml(item.timestamp)}</td>
            <td class="px-3 py-2.5">
                <span onclick="copyToClipboard('${escapeHtml(item.fingerprint)}')" class="cursor-pointer font-mono font-bold text-[11px] text-emerald-800 bg-emerald-50 hover:bg-emerald-100 px-2 py-0.5 rounded-md border border-emerald-200" title="Nusxa olish uchun bosing">
                    ${escapeHtml(item.fingerprint)}
                </span>
            </td>
            <td class="px-3 py-2.5">${tilBadge}</td>
            <td class="px-3 py-2.5">
                <button onclick="viewEntry(${item.id})" class="font-bold text-gray-900 hover:text-emerald-600 text-left transition-colors truncate max-w-[200px] block" title="${escapeHtml(item.fish)}">
                    ${escapeHtml(item.fish)}
                </button>
            </td>
            <td class="px-3 py-2.5">${sinfBadge}</td>
            <td class="px-3 py-2.5 text-gray-700 truncate max-w-[220px]" title="${escapeHtml(item.fanlar)}">${escapeHtml(item.fanlar) || '-'}</td>
            <td class="px-3 py-2.5 text-gray-700 truncate max-w-[220px]" title="${escapeHtml(item.togaraklar)}">${escapeHtml(item.togaraklar) || '-'}</td>
            <td class="px-3 py-2.5 text-gray-700 truncate max-w-[220px]" title="${escapeHtml(item.iqtidor)}">${escapeHtml(item.iqtidor) || '-'}</td>
            <td class="px-3 py-2.5 font-semibold text-blue-800 truncate max-w-[180px]" title="${escapeHtml(item.kasb)}">
                ${escapeHtml(item.kasb) || '-'}
            </td>
            <td class="px-3 py-2.5 text-gray-600 truncate max-w-[220px]" title="${escapeHtml(item.startap)}">${escapeHtml(item.startap) || '-'}</td>
            <td class="px-3 py-2.5 text-emerald-800 font-semibold truncate max-w-[240px]" title="${escapeHtml(item.yangi_togaraklar)}">${escapeHtml(item.yangi_togaraklar) || '-'}</td>
            <td class="px-3 py-2.5 text-gray-600 truncate max-w-[220px]" title="${escapeHtml(item.takliflar)}">${escapeHtml(item.takliflar) || '-'}</td>
            <td class="px-2 py-2.5 text-center sticky right-0 bg-white border-l border-gray-200 shadow-sm">
                <div class="flex items-center justify-center space-x-1">
                    <button onclick="viewEntry(${item.id})" class="p-1.5 text-emerald-700 hover:bg-emerald-50 rounded-lg transition-colors" title="Batafsil">
                        <i data-lucide="eye" class="w-4 h-4"></i>
                    </button>
                    <button onclick="editEntry(${item.id})" class="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" title="Tahrirlash">
                        <i data-lucide="edit-3" class="w-4 h-4"></i>
                    </button>
                    <button onclick="deleteEntry(${item.id})" class="p-1.5 text-red-500 hover:bg-red-50 rounded-lg transition-colors" title="O'chirish">
                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                    </button>
                </div>
            </td>
        </tr>
        `;
    });

    tbody.innerHTML = html;
    lucide.createIcons();
}

function debounceSearch() {
    clearTimeout(searchTimeout);
    const searchVal = document.getElementById('searchInput')?.value.trim();
    const clearBtn = document.getElementById('clearSearchBtn');
    if (clearBtn) {
        if (searchVal) clearBtn.classList.remove('hidden');
        else clearBtn.classList.add('hidden');
    }

    searchTimeout = setTimeout(() => {
        loadEntries();
    }, 250);
}

function clearSearch() {
    const input = document.getElementById('searchInput');
    if (input) input.value = '';
    document.getElementById('clearSearchBtn')?.classList.add('hidden');
    loadEntries();
}

function openAddModal() {
    document.getElementById('entryForm').reset();
    document.getElementById('entryId').value = '';
    document.getElementById('modalTitle').textContent = "Yangi Ma'lumot Kiritish";
    document.getElementById('modalIcon').setAttribute('data-lucide', 'user-plus');
    lucide.createIcons();
    document.getElementById('entryModal').classList.remove('hidden');
}

function closeEntryModal() {
    document.getElementById('entryModal').classList.add('hidden');
}

function appendTag(inputId, text) {
    const input = document.getElementById(inputId);
    if (!input) return;
    let current = input.value.trim();
    if (!current) {
        input.value = text;
    } else {
        const items = current.split(',').map(s => s.trim());
        if (!items.includes(text)) {
            input.value = current + ', ' + text;
        }
    }
}

async function saveEntry(e) {
    e.preventDefault();
    const id = document.getElementById('entryId').value;

    const payload = {
        fish: document.getElementById('inputFish').value.trim(),
        sinf: document.getElementById('inputSinf').value.trim(),
        til: document.getElementById('inputTil').value,
        fanlar: document.getElementById('inputFanlar').value.trim(),
        togaraklar: document.getElementById('inputTogaraklar').value.trim(),
        iqtidor: document.getElementById('inputIqtidor').value.trim(),
        kasb: document.getElementById('inputKasb').value.trim(),
        startap: document.getElementById('inputStartap').value.trim(),
        yangi_togaraklar: document.getElementById('inputYangiTogaraklar').value.trim(),
        takliflar: document.getElementById('inputTakliflar').value.trim()
    };

    if (!payload.fish || !payload.sinf) {
        showToast("F.I.Sh. va Sinf maydonlarini to'ldiring!", "error");
        return;
    }

    try {
        const url = id ? `/api/entries/${id}` : '/api/entries';
        const method = id ? 'PUT' : 'POST';

        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await res.json();
        if (result.status === 'success') {
            showToast(id ? "Ma'lumot yangilandi!" : "Yangi ma'lumot qo'shildi!", "success");
            closeEntryModal();
            loadEntries();
        } else {
            showToast(result.message || "Xatolik yuz berdi", "error");
        }
    } catch (err) {
        console.error(err);
        showToast("Server bilan bog'lanishda xatolik", "error");
    }
}

async function editEntry(id) {
    try {
        const res = await fetch(`/api/entries/${id}`);
        const result = await res.json();
        if (result.status === 'success') {
            const data = result.data;
            document.getElementById('entryId').value = data.id;
            document.getElementById('inputFish').value = data.fish;
            document.getElementById('inputSinf').value = data.sinf;
            document.getElementById('inputTil').value = data.til;
            document.getElementById('inputFanlar').value = data.fanlar || '';
            document.getElementById('inputTogaraklar').value = data.togaraklar || '';
            document.getElementById('inputIqtidor').value = data.iqtidor || '';
            document.getElementById('inputKasb').value = data.kasb || '';
            document.getElementById('inputStartap').value = data.startap || '';
            document.getElementById('inputYangiTogaraklar').value = data.yangi_togaraklar || '';
            document.getElementById('inputTakliflar').value = data.takliflar || '';

            document.getElementById('modalTitle').textContent = `Tahrirlash: ${data.fish}`;
            document.getElementById('modalIcon').setAttribute('data-lucide', 'edit-3');
            lucide.createIcons();

            if (document.getElementById('viewModal')) {
                closeViewModal();
            }
            document.getElementById('entryModal').classList.remove('hidden');
        }
    } catch (err) {
        showToast("Ma'lumotni yuklab bo'lmadi", "error");
    }
}

async function deleteEntry(id) {
    if (!confirm("Haqiqatan ham ushbu yozuvni o'chirmoqchimisiz?")) {
        return;
    }

    try {
        const res = await fetch(`/api/entries/${id}`, { method: 'DELETE' });
        const result = await res.json();
        if (result.status === 'success') {
            showToast("Yozuv o'chirildi", "success");
            loadEntries();
        }
    } catch (err) {
        showToast("O'chirishda xatolik yuz berdi", "error");
    }
}

async function viewEntry(id) {
    currentViewedId = id;
    try {
        const res = await fetch(`/api/entries/${id}`);
        const result = await res.json();
        if (result.status === 'success') {
            const data = result.data;
            document.getElementById('viewFingerprint').textContent = data.fingerprint;
            document.getElementById('viewFish').textContent = data.fish;
            document.getElementById('viewSinf').textContent = data.sinf;
            document.getElementById('viewTil').textContent = data.til;
            document.getElementById('viewTimestamp').textContent = data.timestamp;
            document.getElementById('viewKasb').textContent = data.kasb || '-';
            document.getElementById('viewFanlar').textContent = data.fanlar || '-';
            document.getElementById('viewTogaraklar').textContent = data.togaraklar || '-';
            document.getElementById('viewIqtidor').textContent = data.iqtidor || '-';
            document.getElementById('viewStartap').textContent = data.startap || '-';
            document.getElementById('viewYangiTogaraklar').textContent = data.yangi_togaraklar || '-';
            document.getElementById('viewTakliflar').textContent = data.takliflar || '-';

            document.getElementById('viewModal').classList.remove('hidden');
        }
    } catch (err) {
        showToast("Ma'lumotni ochib bo'lmadi", "error");
    }
}

function closeViewModal() {
    document.getElementById('viewModal').classList.add('hidden');
}

function editCurrentViewed() {
    if (currentViewedId) {
        editEntry(currentViewedId);
    }
}

async function confirmClearAll() {
    if (currentEntries.length === 0) {
        showToast("Jadval allaqachon bo'sh", "info");
        return;
    }
    const check = prompt("DIQQAT: Jadvaldagi barcha ma'lumotlar butunlay o'chiriladi!\nDavom etish uchun 'TOZALASH' so'zini yozing:");
    if (check && check.trim().toUpperCase() === 'TOZALASH') {
        try {
            const res = await fetch('/api/clear', { method: 'POST' });
            const result = await res.json();
            if (result.status === 'success') {
                showToast("Barcha ma'lumotlar tozalandi!", "success");
                loadEntries();
            }
        } catch (err) {
            showToast("Tozalashda xatolik yuz berdi", "error");
        }
    }
}

function toggleExportMenu() {
    const menu = document.getElementById('exportMenu');
    menu.classList.toggle('hidden');
}

// Close export menu when clicking outside
window.addEventListener('click', (e) => {
    if (!e.target.closest('.dropdown')) {
        document.getElementById('exportMenu')?.classList.add('hidden');
    }
});

function clientExcelExport() {
    if (currentEntries.length === 0) {
        showToast("Eksport qilish uchun jadvalda ma'lumot yo'q", "info");
        return;
    }

    const exportData = currentEntries.map(r => ({
        "Sana va vaqt": r.timestamp,
        "Fingerprint": r.fingerprint,
        "Til": r.til,
        "F.I.Sh.": r.fish,
        "Sinf": r.sinf,
        "Qiziqadigan fanlar": r.fanlar,
        "Togaraklar": r.togaraklar,
        "Iqtidor sohasi": r.iqtidor,
        "Kelajak kasbi": r.kasb,
        "Startap loyihasi": r.startap,
        "Yangi togaraklar taklifi": r.yangi_togaraklar,
        "Qoshimcha takliflar": r.takliflar
    }));

    const ws = XLSX.utils.json_to_sheet(exportData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Natijalar");
    XLSX.writeFile(wb, `Sorovnoma_35maktab_${new Date().toISOString().slice(0,10)}.xlsx`);
    showToast("Excel fayli tayyorlandi!", "success");
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast(`Nusxalandi: ${text}`, "success");
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
