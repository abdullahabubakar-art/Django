(function() {
    
    const container = document.createElement('div');
    container.style.padding = '30px';
    container.style.fontFamily = 'Poppins';
    const style = document.createElement('style');
    style.textContent = `
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

        
        body { 
            margin: 0; 
            color: #000;
        }

        .header-title {
            font-size: 27.35px;
            font-style: Medium;
            font-weight: 500;
            margin-bottom: 40px;
           
        }

        .meta-row {
            display: flex;
            align-items: center;
            gap: 40px;
            margin-bottom: 50px;
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .meta-label {
            font-size: 16.28px;
            font-weight: 400;
            color: #000000;
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
            transition: 0.2s;
            position: relative;
        }

        .circle-dashed:hover {
            border-color: #1976d2;
            color: #1976d2;
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
            border: 3.03px solid #FFFFFF;
            margin-right: -20px;
            object-fit: cover;
        }
        
        .user-dropdown {
            position: absolute; top: 45px; left: 80px; background: white;
            border: 1px solid #E5E7EB; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            display: none; z-index: 100; min-width: 160px; overflow: hidden;
        }
        .user-option { 
            display: flex; align-items: center; gap: 10px; padding: 10px; 
            cursor: pointer; font-size: 14px; transition: 0.2s;
        }
        .user-option:hover { background: #F4F4F5; }
        .user-option img { width: 24px; height: 24px; border-radius: 50%; }

        .title-input {
            border: none;
            font-size: 34.45px;
            front-style: Medium;
            font-weight: 500;
            color: #000; 
            margin-bottom: 30px;
            outline: none
        }

        .title-input::placeholder {
         color: #DFDEE0;
         }

        .section-label {
            font-size: 16.28px;
            font-weight: 400;
            color: #000000;
            margin-bottom: 15px;
        }

        .details-box {
            width: 716px;
            height: 53.56px;
            border: 1.02px solid #F4F4F5;
            border-radius: 5.09px;
            padding: 16.28px;
            font-weight: 400;
            font-size: 14.25px;
            margin-bottom: 40px;
            box-sizing: border-box;
        }

        .drop-zone {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 10px;
            cursor: pointer;
            margin-bottom: 185px;
        }

        .drop-text {
            color: #4C535F66;
            font-size: 17.64px;
            font-weight: 500
        }

        .browse-link {
            color: #1D4ED8;
            text-decoration: underline solid;
            
        }

        .footer-actions {
            display: flex;
            justify-content: flex-end;
            padding-top: 20px;
            border-top: 1px solid #F3F4F6;
        }

        .add-btn {
            width: 133px;
            height: 40px;
            background: #007DFA;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
        }
    `;
    document.head.appendChild(style);

    container.innerHTML = `
        <div class="header-title">Add new bug</div>
        
        <div class="meta-row">
            <div class="meta-item">
                <span class="meta-label">Assign to</span>
                <div class="avatar-group">
                    <img id="current-assignee-img" src="http://localhost:8000/media/bugs/Person.jpg" class="avatar">
                    <div class="circle-dashed" id="dropdown-trigger">+</div>
                </div>
                <div class="user-dropdown" id="user-menu">
                    <div class="user-option" data-name="Qasim" data-src="http://localhost:8000/media/bugs/Qasim.jpg">
                        <img src="http://localhost:8000/media/bugs/Qasim.jpg"> Qasim
                    </div>
                    <div class="user-option" data-name="Person" data-src="http://localhost:8000/media/bugs/Person.jpg">
                        <img src="http://localhost:8000/media/bugs/Person.jpg"> Person
                    </div>
                </div>
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

        <div class="section-label">Bug details</div>
        <textarea id="description" class="details-box" placeholder="Add here" ></textarea>

        <div class="drop-zone" id="drop-zone">
            <img src="http://localhost:8000/media/bugs/Upload.png" style="width:50px; margin-bottom:50px;">  
            <div class="drop-text">Drop any file here or <span class="browse-link">browse</span></div>
            <input type="file" id="file-input" style="display:none" accept="image/*">
        </div>

        <div class="footer-actions">
            <button id="submit-btn" class="add-btn">Add</button>
        </div>
    `;

    document.body.appendChild(container);

    const trigger = document.getElementById('dropdown-trigger');
    const menu = document.getElementById('user-menu');
    const assigneeImg = document.getElementById('current-assignee-img');
    let selectedUser = "Person"; // Default

    trigger.onclick = (e) => {
        e.stopPropagation();
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    };

    

    const fileInput = document.getElementById('file-input');
    document.getElementById('drop-zone').onclick = () => fileInput.click();


    document.getElementById('submit-btn').onclick = async () => {
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;

        const formData = new FormData();
        formData.append('title', title);
        formData.append('description', description);
        if(fileInput.files[0]) formData.append('screenshot', fileInput.files[0]);

        try {
            const res = await fetch('http://localhost:8000/api/bugs/', { 
                method: 'POST', 
                body: formData 
            });
            if (res.ok) {
                window.parent.postMessage({ type: 'BUG_CREATED_SUCCESS' }, '*');
            }
        } catch (e) {
            console.error(e);
        }
    };
})();