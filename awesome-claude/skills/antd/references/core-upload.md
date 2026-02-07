---
name: antd-upload
description: Ant Design Upload component for file upload functionality. Use when building file upload features, image uploads, or drag-and-drop file interfaces.
---

# Upload Component

Upload is a core component in Ant Design for file uploads, supporting click upload, drag-and-drop upload, image preview, and more.

## Basic Usage

```tsx
import { Upload, Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const BasicUpload = () => {
  const props = {
    name: 'file',
    action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76',
    headers: {
      authorization: 'authorization-text',
    },
    onChange(info: any) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        console.log(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === 'error') {
        console.log(`${info.file.name} file upload failed.`);
      }
    },
  };

  return (
    <Upload {...props}>
      <Button icon={<UploadOutlined />}>Click to Upload</Button>
    </Upload>
  );
};
```

## Upload Status

Files have the following statuses during upload:

- **uploading** - Uploading
- **done** - Upload successful
- **error** - Upload failed
- **removed** - Removed

```tsx
const handleChange = (info: any) => {
  const { file, fileList } = info;
  
  if (file.status === 'uploading') {
    console.log('Uploading...');
  }
  
  if (file.status === 'done') {
    console.log('Upload success:', file.response);
  }
  
  if (file.status === 'error') {
    console.log('Upload failed:', file.error);
  }
  
  // Update fileList
  setFileList(fileList);
};
```

## Controlled File List

```tsx
import { useState } from 'react';

const ControlledUpload = () => {
  const [fileList, setFileList] = useState([]);

  const handleChange = ({ fileList: newFileList }: any) => {
    setFileList(newFileList);
  };

  return (
    <Upload
      fileList={fileList}
      onChange={handleChange}
      action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
    >
      <Button icon={<UploadOutlined />}>Upload</Button>
    </Upload>
  );
};
```

## Pre-upload Validation

### beforeUpload

```tsx
const beforeUpload = (file: File) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  if (!isJpgOrPng) {
    message.error('You can only upload JPG/PNG file!');
    return false; // Prevent upload
  }
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    message.error('Image must smaller than 2MB!');
    return false;
  }
  return true; // Allow upload
};

<Upload
  name="avatar"
  listType="picture-card"
  className="avatar-uploader"
  showUploadList={false}
  action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
  beforeUpload={beforeUpload}
  onChange={handleChange}
>
  {imageUrl ? <img src={imageUrl} alt="avatar" style={{ width: '100%' }} /> : uploadButton}
</Upload>
```

### Return Promise

```tsx
const beforeUpload = async (file: File) => {
  // Can return Promise for async validation
  const isValid = await validateFile(file);
  if (!isValid) {
    return Upload.LIST_IGNORE; // Ignore file, don't add to list
  }
  return true;
};
```

## Custom Upload Request

```tsx
import type { UploadProps } from 'antd';

const customRequest: UploadProps['customRequest'] = async (options) => {
  const { onSuccess, onError, file, onProgress } = options;

  // Create FormData
  const formData = new FormData();
  formData.append('file', file as File);

  // Use XMLHttpRequest or fetch
  const xhr = new XMLHttpRequest();

  // Upload progress
  xhr.upload.addEventListener('progress', (event) => {
    if (event.lengthComputable) {
      const percent = (event.loaded / event.total) * 100;
      onProgress?.({ percent });
    }
  });

  // Upload success
  xhr.addEventListener('load', () => {
    if (xhr.status === 200) {
      onSuccess?.(xhr.response, xhr);
    } else {
      onError?.(new Error('Upload failed'));
    }
  });

  // Upload failed
  xhr.addEventListener('error', () => {
    onError?.(new Error('Upload failed'));
  });

  xhr.open('POST', 'https://api.example.com/upload');
  xhr.send(formData);
};

<Upload customRequest={customRequest}>
  <Button icon={<UploadOutlined />}>Upload</Button>
</Upload>
```

## Image Upload and Preview

### Image Upload

```tsx
import { Upload, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import type { UploadFile, UploadProps } from 'antd/es/upload/interface';

const getBase64 = (file: File): Promise<string> =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = (error) => reject(error);
  });

const ImageUpload = () => {
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewImage, setPreviewImage] = useState('');
  const [fileList, setFileList] = useState<UploadFile[]>([]);

  const handlePreview = async (file: UploadFile) => {
    if (!file.url && !file.preview) {
      file.preview = await getBase64(file.originFileObj as File);
    }
    setPreviewImage(file.url || (file.preview as string));
    setPreviewOpen(true);
  };

  const handleChange: UploadProps['onChange'] = ({ fileList: newFileList }) => {
    setFileList(newFileList);
  };

  const uploadButton = (
    <div>
      <PlusOutlined />
      <div style={{ marginTop: 8 }}>Upload</div>
    </div>
  );

  return (
    <>
      <Upload
        listType="picture-card"
        fileList={fileList}
        onPreview={handlePreview}
        onChange={handleChange}
        action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
      >
        {fileList.length >= 8 ? null : uploadButton}
      </Upload>
      <Modal open={previewOpen} footer={null} onCancel={() => setPreviewOpen(false)}>
        <img alt="preview" style={{ width: '100%' }} src={previewImage} />
      </Modal>
    </>
  );
};
```

### Limit Upload Count

```tsx
<Upload
  action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
  listType="picture-card"
  maxCount={3} // Maximum 3 files
>
  <div>
    <PlusOutlined />
    <div style={{ marginTop: 8 }}>Upload</div>
  </div>
</Upload>
```

## Drag and Drop Upload

```tsx
import { Upload, message } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';

const { Dragger } = Upload;

const props: UploadProps = {
  name: 'file',
  multiple: true,
  action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76',
  onChange(info) {
    const { status } = info.file;
    if (status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (status === 'done') {
      message.success(`${info.file.name} file uploaded successfully.`);
    } else if (status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  },
  onDrop(e) {
    console.log('Dropped files', e.dataTransfer.files);
  },
};

<Dragger {...props}>
  <p className="ant-upload-drag-icon">
    <InboxOutlined />
  </p>
  <p className="ant-upload-text">Click or drag file to this area to upload</p>
  <p className="ant-upload-hint">
    Support for a single or bulk upload. Strictly prohibited from uploading company data or other
    band files
  </p>
</Dragger>
```

## Upload Properties

### Basic Properties

- **action** (string | (file) => Promise<string>) - Upload URL or function returning URL
- **name** (string) - File parameter name sent to server, default 'file'
- **multiple** (boolean) - Whether to support multiple file selection, default false
- **directory** (boolean) - Whether to support folder upload, default false
- **accept** (string) - Accepted file types, e.g., 'image/*'
- **fileList** (UploadFile[]) - List of uploaded files (controlled)
- **defaultFileList** (UploadFile[]) - Default list of uploaded files

### Upload Behavior

- **beforeUpload** ((file, fileList) => boolean | Promise) - Hook before uploading file
- **customRequest** ((options) => void) - Custom upload implementation
- **data** (object | (file) => object | Promise<object>) - Additional upload parameters or function returning parameters
- **headers** (object) - Request headers
- **method** (string) - HTTP method for upload request, default 'post'
- **withCredentials** (boolean) - Whether to send cookies with upload request, default false

### Display Configuration

- **listType** ('text' | 'picture' | 'picture-card' | 'picture-circle') - Built-in styles for upload list
- **showUploadList** (boolean | object) - Whether to show upload list
- **maxCount** (number) - Limit upload count
- **disabled** (boolean) - Whether disabled, default false

### Callback Functions

- **onChange** ((info) => void) - Callback when upload state changes
- **onPreview** ((file) => void) - Callback when clicking file link or preview icon
- **onRemove** ((file) => boolean | Promise<boolean>) - Callback when clicking remove button
- **onDownload** ((file) => void) - Callback when clicking download button
- **onDrop** ((event) => void) - Callback when files are dropped

### UploadFile Type

```tsx
interface UploadFile {
  uid: string;                    // Unique identifier
  name: string;                   // File name
  status?: 'uploading' | 'done' | 'error' | 'removed'; // Upload status
  response?: string;               // Server response content
  error?: any;                    // Error information
  url?: string;                   // File URL
  percent?: number;               // Upload progress percentage
  originFileObj?: File;          // Original file object
  thumbUrl?: string;              // Thumbnail URL
}
```

## Best Practices

1. **File validation** - Use beforeUpload to validate file type and size
2. **Custom upload** - Use customRequest to implement custom upload logic
3. **Controlled component** - Use fileList and onChange to implement controlled upload
4. **Image preview** - Use onPreview to implement image preview functionality
5. **Error handling** - Properly handle upload failure cases
6. **User experience** - Display upload progress and status feedback

<!--
Source references:
- https://ant.design/components/upload-cn
- https://github.com/ant-design/ant-design/blob/master/components/upload/index.en-US.md
-->
