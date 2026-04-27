/*
  Firebase Storage helper for Sylva Lens uploads.
  Replace the placeholder values below with your Firebase project settings.
*/

const firebaseConfig = window.FIREBASE_CONFIG;
const FIREBASE_CONFIGURED = firebaseConfig && firebaseConfig.apiKey && !firebaseConfig.apiKey.includes('YOUR_');
let firebaseStorage = null;

if (FIREBASE_CONFIGURED) {
    const app = firebase.initializeApp(firebaseConfig);
    firebaseStorage = firebase.storage(app);
} else {
    console.warn('Firebase is not configured in firebase-upload.js. Uploads will remain local-only.');
}

function dataURLToBlob(dataURL) {
    const parts = dataURL.split(';base64,');
    const contentType = parts[0].split(':')[1];
    const raw = window.atob(parts[1]);
    const rawLength = raw.length;
    const array = new Uint8Array(rawLength);
    for (let i = 0; i < rawLength; i++) {
        array[i] = raw.charCodeAt(i);
    }
    return new Blob([array], { type: contentType });
}

async function uploadImageToFirebase(category, fileName, dataUrl) {
    if (!firebaseStorage) {
        return { url: dataUrl, path: null };
    }

    const blob = dataURLToBlob(dataUrl);
    const safeName = fileName.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9._-]/g, '');
    const storagePath = `uploads/${category}/${Date.now()}_${safeName}`;
    const uploadRef = firebaseStorage.ref(storagePath);
    const snapshot = await uploadRef.put(blob, { contentType: 'image/jpeg' });
    const url = await snapshot.ref.getDownloadURL();
    return { url, path: storagePath };
}

async function listFirebaseUploads(category) {
    if (!firebaseStorage) {
        return [];
    }

    try {
        const listRef = firebaseStorage.ref(`uploads/${category}`);
        const result = await listRef.listAll();
        const uploads = await Promise.all(result.items.map(async itemRef => ({
            url: await itemRef.getDownloadURL(),
            name: itemRef.name,
            path: itemRef.fullPath
        })));
        return uploads;
    } catch (error) {
        console.error('Firebase storage list error:', error);
        return [];
    }
}

async function deleteFirebaseImage(storagePath) {
    if (!firebaseStorage || !storagePath) {
        return false;
    }

    try {
        await firebaseStorage.ref(storagePath).delete();
        return true;
    } catch (error) {
        console.error('Firebase delete error:', error);
        return false;
    }
}

async function loadRemoteImages(category, portfolioGrid, uploadSlot) {
    if (!firebaseStorage || !portfolioGrid || !uploadSlot) {
        return;
    }

    const existingUrls = new Set(Array.from(portfolioGrid.querySelectorAll('.portfolio-item'))
        .reduce((urls, item) => {
            const bg = item.style.backgroundImage;
            const bgMatch = bg.match(/url\(["']?(.*?)["']?\)/);
            if (bgMatch && bgMatch[1]) {
                urls.push(bgMatch[1]);
            }
            const dataSrc = item.getAttribute('data-src');
            if (dataSrc) {
                urls.push(dataSrc);
            }
            return urls;
        }, [])
        .filter(Boolean));

    const remoteImages = await listFirebaseUploads(category);
    remoteImages.forEach(itemData => {
        if (existingUrls.has(itemData.url)) {
            return;
        }

        const newItem = document.createElement('div');
        newItem.className = 'portfolio-item lazy-loading';
        newItem.setAttribute('data-src', itemData.url);
        newItem.setAttribute('data-loaded', 'false');
        if (itemData.path) {
            newItem.setAttribute('data-path', itemData.path);
        }
        newItem.innerHTML = '<div class="image-placeholder"><div class="loading-spinner"></div></div>';
        portfolioGrid.insertBefore(newItem, uploadSlot);
        newItem.addEventListener('click', function () {
            if (typeof handlePortfolioClick === 'function') {
                handlePortfolioClick(this);
            }
        });

        if (typeof addRemoveButton === 'function') {
            addRemoveButton(newItem, category, itemData.url, itemData.path);
        }
    });
}
