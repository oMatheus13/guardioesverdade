const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  const { path: requestedPath } = req.query;
  let filePath;

  // Helper function to send file content
  const sendFileContent = (filePath) => {
    fs.readFile(filePath, (err, data) => {
      if (err) {
        console.error('Error reading file:', err);
        return res.status(500).send('<h1>500: Internal Server Error</h1>');
      }
      res.status(200).setHeader('Content-Type', 'text/html'); // Set content type
      res.send(data);
    });
  };

  // If the requested path is empty (root path), serve the main index.html
  if (!requestedPath) {
    filePath = path.join(process.cwd(), 'index.html');
    if (fs.existsSync(filePath)) {
      return sendFileContent(filePath);
    }
  } else {
    // Check if the requested path exists as a file in 'pages' directory
    filePath = path.join(process.cwd(), 'pages', `${requestedPath}.html`);
    if (fs.existsSync(filePath)) {
      return sendFileContent(filePath);
    }

    // Check if the requested path exists as a file in 'fragments' directory
    filePath = path.join(process.cwd(), 'fragments', requestedPath, 'index.html');
    if (fs.existsSync(filePath)) {
      return sendFileContent(filePath);
    }
  }

  // If no file is found, return the custom 404 page
  const notFoundPath = path.join(process.cwd(), 'pages', '404.html');
  if (fs.existsSync(notFoundPath)) {
    return sendFileContent(notFoundPath);
  }

  // If the custom 404 page is not found, return a basic 404 error
  return res.status(404).send('<h1>404: Página Não Encontrada</h1>');
};
