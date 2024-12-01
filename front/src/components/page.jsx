import React, { useState } from 'react';
import './style.css';

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');
  const [responseText, setResponseText] = useState('');
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setMessage('json файл');
  };

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
    setMessage('контекст');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file || !selectedOption) {
      setMessage('Пожалуйста, выберите json файл и вариант контекста.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('textOption', selectedOption); // Передаем выбранный текст

    try {
      const response = await fetch('http://localhost:8000/uploadjson/', {
        method: 'POST',
        body: formData,
        requestConfig: {contentType: "application/json"},
        headers: {contentType: "application/json"}
      });
      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.status}`);
      }

      const data = await response.text();
      const data1 = JSON.parse(data)

      if (selectedOption === 'option1'){
        setResponseText(data1.message_on_entry);
      }
      else if (selectedOption === 'option2'){
        setResponseText(data1.message_after_oper);
      }
      else if(selectedOption === 'option3'){
        setResponseText(data1.message_before_vip_oper)
      }
      setMessage('Данные успешно отправлены!');

    } catch (error) {
      console.error('Ошибка:', error);
      setMessage('Ошибка отправки данных.');
    }
  };

  return (
    <div className="uploader-container">
      <h1>Загрузите JSON файл и выберите контекст</h1>
      
      <form onSubmit={handleSubmit}>
        <div className="drop-area">
          <label htmlFor="fileInput">Выберите JSON файл:</label>
          <input
            id="fileInput"
            type="file"
            accept=".json"
            onChange={handleFileChange}
          />
        </div>
        
        <div className="option-selector">
          <label htmlFor="textOption">Выберите контекст:</label>
          <select id="textOption" value={selectedOption} onChange={handleOptionChange}>
            <option value="">--Выберите вариант--</option>
            <option value="option1">При запуске</option>
            <option value="option2">При совершении обычной операции</option>
            <option value="option3">При совершении операции повышенной важности</option>
          </select>
        </div>

        <button type="submit" className="submit-btn">Отправить</button>
      </form>

      {message && <p className="message">{message}</p>}
      {responseText && <div className="response-text">{responseText}</div>}
    </div>
  );
};

export default FileUploader;
