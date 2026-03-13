(function() {
    
    const container = document.createElement('div');
    container.style.fontFamily = 'Poppins';
    const style = document.createElement('style');
    container.style.display = 'flex';
    container.style.flexDirection = 'column';
    container.style.height = '100vh';
    style.textContent = `
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

        
       body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; }

        .main-wrapper {
            flex: 1;
            overflow-y: auto;
            padding-bottom: 80px;
        }

        .header-section { padding: 30px 33px 0 33px; }  
        .header-title {
            font-family: 'Poppins';
            font-size: 27.35px;
            font-weight: 500;
            margin-bottom: 28px;
        }
        .header-line { width: 100%; height: 1px; background: #ECECEE; margin-bottom: 30px; }

        .meta-row { display: flex; gap: 140px; padding: 0 33px; margin-bottom: 40px; }
        .meta-item { display: flex; align-items: center; gap: 15px; position: relative; }
        
        .meta-label {
            font-family: 'Poppins';
            font-weight: 400;
            font-size: 16.28px;
            line-height: 100%;
            color: #000;
            white-space: nowrap;
        }

        .circle-dashed {
            width: 36.35px;
            height: 36.35px;
            border: 2.03px dashed #94A3B8;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            color: #94A3B8;
            position: relative;
        }

        .circle-dashed:hover {
            border-color: #1976d2;
            color: #1976d2;
        }
        
        .selection-text {
            font-family: 'Poppins';
            font-size: 14px;
            font-weight: 500;
            color: #4A5568;
        }
            
        .date-input-hidden {
            position: absolute; opacity: 0; width: 100%; height: 100%; cursor: pointer;
        }

        .avatar-group {
            display: flex;
            align-items: center;
        }

        .avatar {
            width: 36.35px;
            height: 36.35px;
            border-radius: 50%;
            margin-right: -20px;
            object-fit: cover;
        }
        
        .user-dropdown {
            position: absolute;
            top: 45px;
            left: 80px; 
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            display: none; 
            z-index: 1000; 
            min-width: 180px;
            max-height: 200px; 
            overflow-y: auto;
        }
        .user-option { 
            display: flex; align-items: center; gap: 10px; padding: 10px; 
            cursor: pointer; font-size: 14px; transition: 0.2s;
        }
        .user-option:hover { background: #F4F4F5; }
        .user-option img { width: 24px; height: 24px; border-radius: 50%; }

        .title-input {
            border: none;
            font-family: 'Poppins';
            font-size: 34.45px;
            font-weight: 500;
            font-style: Medium;
            outline: none;
            margin: 0 33px 30px 33px;
            outline: none
        }

        .title-input::placeholder {
         color: #DFDEE0;
         }

        .section-container { padding: 0 33px; }
        .section-label {
            font-family: 'Poppins';
            font-weight: 400;
            font-size: 16.28px;
            margin-bottom: 15px;
        }

        .details-box {
          width: 100%;
            max-width: 716px;
            height: 53px; 
            border: 1.02px solid #F4F4F5;
            border-radius: 5.09px;
            font-weight: 400;
            font-size: 14.25px;
            margin-bottom: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            cursor: pointer;
            padding: 16.28px;
            box-sizing: border-box;
        }

         .details-box::placeholder {
          font-family: 'Poppins';
            font-size: 14.25px;
            font-weight: 400;
         color: #000 
         }


        .drop-zone {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 10px;
            cursor: pointer;
            border: 1px dashed #F4F4F5
            margin-bottom: 185px;
        }
        .drop-content { display: flex; align-items: center; gap: 15px; }
        .drop-icon { width: 24px; height: 24px; }
        .drop-text {
            font-family: 'Poppins';
            color: #4C535F66;
            font-size: 17.64px;
            font-weight: 500
            font-style:Medium
        }

        .browse-link {
            color: #1D4ED8;
            text-decoration: underline solid;
            
        }

        .preview-img-full {
            max-height: 200px; 
            max-width: 200px; 
            border-radius: 4px; 
            object-fit: contain;
        }
        .footer-actions {
           position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 71px;
            background: #FFFFFF;
            border-top: 1px solid #F3F4F6;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 33px;
            box-sizing: border-box;
            z-index: 100;
        }

        .add-btn {
         width: 133px;
            height: 40px;
            background: #007DFA;
            color: white;
            border: none;
            border-radius: 6px;
            font-family: 'Poppins';
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
        }
    `;
    document.head.appendChild(style);

    container.innerHTML = `
        <div class="main-wrapper">
           <div class="header-section"><div class="header-title">Add new bug</div></div>
            <div class="header-line"></div>
            
            <div class="meta-row">
                <div class="meta-item">
                    <span class="meta-label">Assign to</span>
                    <div class="avatar-group">
                        <img id="current-assignee-img"  id="dropdown-trigger" src="" class="avatar" style="display:none; ">
                        <div class="circle-dashed" id="dropdown-trigger">+</div>
                        <span id="assignee-name" class="selection-text"></span>
                    </div>
                    <div class="user-dropdown" id="user-menu"><div class="user-option"></div></div>
                </div>

                  
                
                <div class="meta-item">
                    <span class="meta-label">Add due date</span>
                    <div class="circle-dashed"> 
                        <img src="http://localhost:8000/media/bugs/Vector.png" style="width:20px;">
                        <input type="date" id="due-date" class="date-input-hidden">
                    </div>
                    <span id="date-display" style="font-size: 12px; color: #94A3B8;"></span>
                </div>
            </div>

            <input type="text" id="title" class="title-input" placeholder="Add title here">
            <div class="section-container">
                <div class="section-label">Bug details</div>
                <textarea id="description" class="details-box" placeholder="Add here" ></textarea>

                <div class="drop-zone" id="drop-zone">
                    <div id="drop-placeholder" class="drop-content">
                        <img src="http://localhost:8000/media/bugs/Upload.png" class="drop-icon">
                        <div class="drop-text">Drop any file here or <span class="browse-link">browse</span></div>
                    </div>
                    <input type="file" id="file-input" style="display:none" accept="image/*">
                </div>
            </div>
        </div>

        <div class="footer-actions">
            <button id="submit-btn" class="add-btn">Add</button>
        </div>
    `;

    document.body.appendChild(container);

    let selectedDeveloperId = null;
    let currentProjectId = null;
    let bugMetadata = { status_choices: [], type_choices: [] };
    const trigger = document.getElementById('dropdown-trigger');
    const menu = document.getElementById('user-menu');
    const assigneeImg = document.getElementById('current-assignee-img');
    const assigneeNameText = document.getElementById('assignee-name');

    trigger.onclick = (e)=>{
        e.stopPropagation();
        const isVisible = menu.style.display === 'block'
        menu.style.display = isVisible ? 'none': "block";
    }

    window.addEventListener('message', (event) => {
        if (event.data.type === 'SET_DEVELOPER_LIST') {
            menu.innerHTML = ''; 

            currentProjectId = event.data.projectId;
            event.data.developers.forEach(dev => {
                const item = document.createElement('div');
                item.className = 'user-option';
                item.innerHTML = `
                <img src="${dev.avatar}" style="width:24px; height:24px; border-radius:50%">
                <span>${dev.name}</span>`;
                
                item.onclick = (e) => {
                    e.stopPropagation();
                    selectedDeveloperId = dev.id; 
                    assigneeImg.src = dev.avatar;
                    assigneeImg.style.display = 'block';
                    assigneeNameText.innerText = dev.name; 
                    // trigger.style.display = 'none';
                    menu.style.display = 'none';
                };
                menu.appendChild(item);
            });
        }
    });

    window.onclick = () => {
    menu.style.display = 'none';
    };

    document.getElementById('due-date').onchange=(e)=>{
        document.getElementById('date-display').innerText = e.target.value
    }
    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const dropPlaceholder = document.getElementById('drop-placeholder');

    dropZone.onclick = () => fileInput.click();

    fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                dropPlaceholder.innerHTML = `<img src="${event.target.result}" class="preview-img-full">`;
            };
            reader.readAsDataURL(file);
        }
    };

    document.getElementById('submit-btn').onclick = async () => {
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const deadline = document.getElementById('due-date').value;
        const defaultStatus = bugMetadata.status_choices.find(c => c.value === 'new')?.value 
                              || bugMetadata.status_choices[0]?.value;
        
        const defaultType = bugMetadata.type_choices.find(c => c.value === 'bug')?.value 
                            || bugMetadata.type_choices[0]?.value;

        const formData = new FormData();
        formData.append('title', title);
        formData.append('description', description);
        formData.append('assigned_to', selectedDeveloperId) 
        formData.append('deadline', deadline);
        formData.append('project', currentProjectId);
        formData.append('status', defaultStatus); 
        formData.append('type', defaultType);

        if(fileInput.files[0]) formData.append('screenshot', fileInput.files[0]);

        try {
            const res = await fetch('http://localhost:8000/api/bugs/', { 
                method: 'POST', 
                body: formData,
                credentials: 'include',
                headers: { 'X-CSRFToken': getCookie('csrftoken') }
            });
            if (res.ok) {
                window.parent.postMessage({ type: 'BUG_CREATED_SUCCESS' }, '*');
            }
        } catch (e) {
            console.error(e);
        }
    };


    async function loadMetadata() {
        try {
            const response = await fetch('http://localhost:8000/api/bug-metadata/');
            bugMetadata = await response.json();
            console.log("Loaded Metadata:", bugMetadata);
        } catch (e) {
            console.error("Failed to load bug metadata", e);
        }
    }
    loadMetadata();
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

