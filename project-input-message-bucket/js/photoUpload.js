function uploadPhoto() {
    const inputPicture = document.getElementById('picture').files;

    if (inputPicture.length > 0) {
        const fileToLoad = inputPicture[0];
        const fileReader = new FileReader();

        fileReader.onload = function(fileLoadedEvent) {
            const srcData = fileLoadedEvent.target.result;

            const indexOfData = srcData.indexOf(",/9j/");
            const data = srcData.substring(indexOfData + 1);

            const apigClient2 = apigClientFactory.newClient();

            const params = {
                'name': fileToLoad.name,
                // 'Content-Type': `image/${fileName.substring(fileName.indexOf(".") + 1)}`
            };

            apigClient2.photosNamePut(params, data).then(response => {
                alert("Photo upload succeeded!");
            }).catch(error => {
                alert(`Upload failed due to ${JSON.stringify(error)}`);
            });

        };
        fileReader.readAsDataURL(fileToLoad);
    }

    document.getElementById("picture").value = "";
}