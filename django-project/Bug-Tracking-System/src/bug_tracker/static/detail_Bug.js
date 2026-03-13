
(function() {
    const container = document.createElement('div');
    const style = document.createElement('style');
    style.textContent = `
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600&display=swap');

        body { font-family: 'Poppins', sans-serif; margin: 0; padding: 0; background: #fff; overflow-x: hidden; }
        
        .update-header {
            display: flex; align-items: center; justify-content: space-between;
            padding: 15px 33px; border-bottom: 1px solid #8D98AA4D; height: 71px;
            box-sizing: border-box;
        }

        .status-dropdown {
            background: #EEF4FF; color: #3069FE; padding: 4.24px 8.48px 4.24px 8.48px; gap: 8.48px;
            border-radius: 6px; font-family: 'Poppins'; font-size: 16.72px; font-weight: 500; font-style: "SemiBold"
            cursor: pointer; border: none; outline: none;
        }

        .meta-group { display: flex; align-items: center; gap: 15px; }

        .assignee-section { position: relative; display: flex; align-items: center; gap: 12px; }
        .avatar-group { display: flex; align-items: center; cursor: pointer; gap: 10px; }
        .avatar { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 2px solid #fff; }
        
        .selection-text {
            font-family: 'Poppins';
            font-size: 14px;
            font-weight: 500;
            color: #4A5568;
        }

        .user-dropdown {
            position: absolute; top: 45px; left: 0; background: white;
            border: 1px solid #E5E7EB; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            display: none; z-index: 1000; min-width: 200px; max-height: 250px; overflow-y: auto;
        }
        .user-option { display: flex; align-items: center; gap: 10px; padding: 10px; cursor: pointer; }
        .user-option:hover { background: #F4F4F5; }

        .date-container { display: flex; align-items: center; gap: 15px; }
        .vertical-line { width: 1px; height: 37px; background: #ECECEE; }
        .date-info { text-align: right; color: #94A3B8; font-size: 11px; font-weight: 400; text-transform: uppercase; }
        .date-val { color: #475569; font-weight: 500; font-size: 13px; display: block; }

        .circle-dashed {
            width: 36px; height: 36px; border: 2px dashed #94A3B8;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            cursor: pointer; color: #94A3B8; position: relative;
        }

        .content-body { 
            padding: 33px; 
            display: flex; 
            flex-direction: column; 
            align-items: center; /* This centers the children horizontally */
            width: 100%;
            box-sizing: border-box;
        }

        .bug-title {
            width: 100%; max-width: 934px; font-family: 'Poppins'; font-size: 27px;
            font-weight: 600; border: none; margin-bottom: 25px; outline: none; color: #000;
        }

        .image-placeholder-box {
            width: 100%; 
            max-width: 934px; 
            height: 140px; 
            border: 2px dashed #4C535F;
            border-radius: 12px; 
            display: flex; 
            flex-direction: column;
            align-items: center; 
            justify-content: center; 
            color: #4C535F; 
            cursor: pointer;
            margin-bottom: 25px; 
            transition: background 0.2s;
        }
        .image-placeholder-box:hover { background: #F8FAFC; }

        .details-wrapper { width: 100%; max-width: 934px; }
        .details-label { font-size: 16px; font-weight: 500; margin-bottom: 10px; color: #000; }
        .details-textarea {
            width: 100%; height: 138px; border: 1px solid #4C73994D;
            border-radius: 6px; padding: 16px; font-family: 'Poppins';
            font-size: 14px; outline: none; color: #1E293B; box-sizing: border-box; resize: none;
        }

        .footer-actions {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 71px;
            background: #FFFFFF; border-top: 1px solid #F3F4F6;
            display: flex; align-items: center; padding: 0 33px; box-sizing: border-box;
        }
        
        .hidden-input { display: none; }
    `;
    document.head.appendChild(style);

    container.innerHTML = `
        <div class="update-header">
            <div style="display:flex; align-items:center; gap:15px;">
                <select id="status-select" class="status-dropdown"></select>
                <div class="assignee-section">
                    <div class="avatar-group" id="dropdown-trigger">
                        <img id="current-assignee-img" src="" class="avatar" style="display:none;">
                        <div id="assignee-placeholder" class="circle-dashed">+</div>
                        <span id="assignee-name" class="selection-text"></span>
                    </div>
                    <div class="user-dropdown" id="user-menu"></div>
                </div>
            </div>
            
            <div class="meta-group">
                <div class="date-container">
                    <div class="date-info">
                        CREATED <span class="date-val" id="deadline">--</span>
                    </div>
                    <div class="vertical-line"></div>
                    <div class="circle-dashed">
                        <img src="http://localhost:8000/media/bugs/Vector.png" style="width:18px;">
                        <input type="date" id="due-date" class="hidden-input" style="display:block; position:absolute; opacity:0; width:100%; height:100%;">
                    </div>
                </div>
            </div>
        </div>

        <div class="content-body">
            <input type="text" id="title" class="bug-title" placeholder="Bug Title">
            
            <div class="image-placeholder-box" id="drop-zone-main">
                <img src="http://localhost:8000/media/bugs/gallery-add.png" style="width:44px;">
                <span style="font-family:'Manrope'; font-weight:500; margin-top:12px;">Add image here</span>
                <input type="file" id="file-input" class="hidden-input">
            </div>
            <div class="details-wrapper">
                <div class="details-label">Bug details</div>
                <textarea id="description" class="details-textarea" placeholder="Add details..."></textarea>
            </div>
        </div>

        <div class="footer-actions" id="footer-upload-trigger">
                <img src="http://localhost:8000/media/bugs/Upload.png" style="width:24px;">
                <span style="color:#4C535F66; font-size:16px; font-weight:500;">
                    Drop any file here or <span style="color:#1D4ED8; text-decoration:underline;">browse</span>
                </span>
        </div>
    `;
    document.body.appendChild(container);

    let bugId = null;
    let selectedDeveloperId = null;
    const menu = document.getElementById('user-menu');
    const devTrigger = document.getElementById('dropdown-trigger');

    devTrigger.onclick = (e) => {
        e.stopPropagation();
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    };

    window.onclick = () => menu.style.display = 'none';

    window.addEventListener('message', (event) => {
        const data = event.data;
        if (data.type === 'SET_EDIT_MODE') {
            bugId = data.bug.id;
            document.getElementById('title').value = data.bug.title || "";
            document.getElementById('description').value = data.bug.description || "";
            document.getElementById('deadline').innerText = data.bug.deadline || '';
            
            if(data.bug.deadline) document.getElementById('due-date').value = data.bug.deadline;

            if(data.bug.assigned_to_details) {
                updateAssigneeUI(data.bug.assigned_to_details.avatar, data.bug.assigned_to_details.name);
                selectedDeveloperId = data.bug.assigned_to_details.id;
            }

            renderStatuses(data.statusChoices, data.bug.status);
            renderDevelopers(data.developers);
        }
    });

    function renderDevelopers(devs) {
        menu.innerHTML = '';
        devs.forEach(dev => {
            const item = document.createElement('div');
            item.className = 'user-option';
            item.innerHTML = `<img src="${dev.avatar}" class="avatar" style="width:24px; height:24px; margin:0"><span>${dev.name}</span>`;
            item.onclick = () => {
                updateAssigneeUI(dev.avatar, dev.name);
                updateField('assigned_to', dev.id);
            };
            menu.appendChild(item);
        });
    }

    function updateAssigneeUI(avatarUrl, name) {
        const img = document.getElementById('current-assignee-img');
        const plus = document.getElementById('assignee-placeholder');
        const nameText = document.getElementById('assignee-name');
        
        img.src = avatarUrl;
        img.style.display = 'block';
        plus.style.display = 'none';
        nameText.innerText = name;
    }

    function renderStatuses(choices, current) {
        const select = document.getElementById('status-select');
        select.innerHTML = '';
        choices.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.value;
            opt.innerText = c.label;
            if (c.value === current) opt.selected = true;
            select.appendChild(opt);
        });
    }

    document.getElementById('title').onblur = (e) => updateField('title', e.target.value);
    document.getElementById('description').onblur = (e) => updateField('description', e.target.value);
    document.getElementById('status-select').onchange = (e) => updateField('status', e.target.value);
    document.getElementById('due-date').onchange = (e) => updateField('deadline', e.target.value);

    const fInput = document.getElementById('file-input');
    document.getElementById('drop-zone-main').onclick = () => fInput.click();
    document.getElementById('footer-upload-trigger').onclick = () => fInput.click();
    
    fInput.onchange = (e) => {
        if (e.target.files[0]) updateField('screenshot', e.target.files[0]);
    };

    async function updateField(fieldName, value) {
        if (!bugId) return;
        const formData = new FormData();
        formData.append(fieldName, value);
        try {
            const res = await fetch(`http://localhost:8000/api/bugs/${bugId}/`, {
                method: 'POST',
                body: formData,
                credentials: 'include',
                headers: { 'X-CSRFToken': getCookie('csrftoken') }
            });
            if (res.ok) window.parent.postMessage({ type: 'FIELD_UPDATED', field: fieldName }, '*');
        } catch (e) { console.error(e); }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})();