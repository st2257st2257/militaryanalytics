import jsyaml from 'js-yaml';

class FileHandler {
  static saveFile(fileName, data) {
    const fileType = this.getFileType(fileName);
    let formattedData;
    
    if (fileType === 'application/json') {
      formattedData = JSON.stringify(data);
    } else if (fileType === 'text/yaml') {
      formattedData = JSON.stringify(jsyaml.load(data));
    } else {
      formattedData = data;
    }

    sessionStorage.setItem(fileName, formattedData);
  }

  static getFile(fileName) {
    const data = sessionStorage.getItem(fileName);
    return data ? JSON.parse(data) : null;
  }

  static getFileType(fileName) {
    const extension = fileName.split('.').pop().toLowerCase();

    switch (extension) {
      case 'json':
        return 'application/json';
      case 'yaml':
      case 'yml':
        return 'text/yaml';
      default:
        return '';
    }
  }

  static async handleFile(file) {
    if (!file) return;
    const fileName = file.name;
    const fileSize = file.size;
    const fileType = file.type;
    let fileData;

    // Обработка различных типов файлов
    if (fileType === 'application/json') {
      fileData = await file.text().then(data => JSON.parse(data));
    } else if (fileType === 'text/yaml') {
      fileData = await file.text();
    } else {
      fileData = await file.text();
    }

    this.saveFile(fileName, fileData);

    return {
      fileName,
      fileSize,
      fileType,
      fileData
    };
  }
}

export default FileHandler;
