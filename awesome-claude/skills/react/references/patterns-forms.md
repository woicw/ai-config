---
name: forms
description: Controlled components, form handling, and validation
---

# Forms and Inputs

React handles forms differently than plain HTML. Form elements naturally maintain their own state, but in React, we typically use controlled components.

## Controlled Components

### Text Input

```jsx
function NameForm() {
  const [name, setName] = useState('')
  
  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Submitted:', name)
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button type="submit">Submit</button>
    </form>
  )
}
```

### Textarea

```jsx
function MessageForm() {
  const [message, setMessage] = useState('')
  
  return (
    <form>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        rows={4}
      />
    </form>
  )
}
```

### Select

```jsx
function SelectForm() {
  const [fruit, setFruit] = useState('apple')
  
  return (
    <form>
      <select value={fruit} onChange={(e) => setFruit(e.target.value)}>
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </select>
    </form>
  )
}
```

### Checkbox

```jsx
function CheckboxForm() {
  const [agreed, setAgreed] = useState(false)
  
  return (
    <form>
      <label>
        <input
          type="checkbox"
          checked={agreed}
          onChange={(e) => setAgreed(e.target.checked)}
        />
        I agree to the terms
      </label>
    </form>
  )
}
```

### Radio Buttons

```jsx
function RadioForm() {
  const [size, setSize] = useState('medium')
  
  return (
    <form>
      <label>
        <input
          type="radio"
          value="small"
          checked={size === 'small'}
          onChange={(e) => setSize(e.target.value)}
        />
        Small
      </label>
      <label>
        <input
          type="radio"
          value="medium"
          checked={size === 'medium'}
          onChange={(e) => setSize(e.target.value)}
        />
        Medium
      </label>
      <label>
        <input
          type="radio"
          value="large"
          checked={size === 'large'}
          onChange={(e) => setSize(e.target.value)}
        />
        Large
      </label>
    </form>
  )
}
```

---

## Multiple Inputs

### Using Object State

```jsx
function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  })
  
  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }
  
  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Form data:', formData)
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Name"
      />
      <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="Email"
      />
      <textarea
        name="message"
        value={formData.message}
        onChange={handleChange}
        placeholder="Message"
      />
      <button type="submit">Send</button>
    </form>
  )
}
```

---

## Form Validation

### Basic Validation

```jsx
function SignupForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState({})
  
  const validate = () => {
    const newErrors = {}
    
    if (!email) {
      newErrors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Email is invalid'
    }
    
    if (!password) {
      newErrors.password = 'Password is required'
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters'
    }
    
    return newErrors
  }
  
  const handleSubmit = (e) => {
    e.preventDefault()
    
    const validationErrors = validate()
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors)
      return
    }
    
    setErrors({})
    console.log('Form is valid!')
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>
      
      <div>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>
      
      <button type="submit">Sign Up</button>
    </form>
  )
}
```

### Real-time Validation

```jsx
function EmailInput() {
  const [email, setEmail] = useState('')
  const [touched, setTouched] = useState(false)
  
  const isValid = /\S+@\S+\.\S+/.test(email)
  const showError = touched && !isValid && email.length > 0
  
  return (
    <div>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        onBlur={() => setTouched(true)}
        className={showError ? 'input-error' : ''}
      />
      {showError && <span className="error">Invalid email</span>}
    </div>
  )
}
```

---

## File Upload

```jsx
function FileUpload() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)
    
    if (selectedFile) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(selectedFile)
    }
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    const formData = new FormData()
    formData.append('file', file)
    
    await fetch('/api/upload', {
      method: 'POST',
      body: formData
    })
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        onChange={handleFileChange}
        accept="image/*"
      />
      {preview && <img src={preview} alt="Preview" />}
      <button type="submit" disabled={!file}>Upload</button>
    </form>
  )
}
```

---

## Form Submission

### Basic POST

```jsx
function ContactForm() {
  const [formData, setFormData] = useState({ name: '', email: '' })
  const [submitting, setSubmitting] = useState(false)
  const [success, setSuccess] = useState(false)
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      
      if (response.ok) {
        setSuccess(true)
        setFormData({ name: '', email: '' })
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setSubmitting(false)
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
      />
      <input
        name="email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
      />
      <button type="submit" disabled={submitting}>
        {submitting ? 'Sending...' : 'Send'}
      </button>
      {success && <p>Message sent successfully!</p>}
    </form>
  )
}
```

---

## Form Libraries

### React Hook Form

```jsx
import { useForm } from 'react-hook-form'

function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm()
  
  const onSubmit = (data) => {
    console.log(data)
  }
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('email', {
          required: 'Email is required',
          pattern: {
            value: /\S+@\S+\.\S+/,
            message: 'Invalid email'
          }
        })}
      />
      {errors.email && <span>{errors.email.message}</span>}
      
      <input
        type="password"
        {...register('password', {
          required: 'Password is required',
          minLength: {
            value: 6,
            message: 'Password must be at least 6 characters'
          }
        })}
      />
      {errors.password && <span>{errors.password.message}</span>}
      
      <button type="submit">Sign Up</button>
    </form>
  )
}
```

### Formik

```jsx
import { useFormik } from 'formik'

function ContactForm() {
  const formik = useFormik({
    initialValues: {
      name: '',
      email: ''
    },
    validate: (values) => {
      const errors = {}
      
      if (!values.name) {
        errors.name = 'Required'
      }
      
      if (!values.email) {
        errors.email = 'Required'
      } else if (!/\S+@\S+\.\S+/.test(values.email)) {
        errors.email = 'Invalid email'
      }
      
      return errors
    },
    onSubmit: (values) => {
      console.log(values)
    }
  })
  
  return (
    <form onSubmit={formik.handleSubmit}>
      <input
        name="name"
        value={formik.values.name}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
      />
      {formik.touched.name && formik.errors.name && (
        <span>{formik.errors.name}</span>
      )}
      
      <input
        name="email"
        value={formik.values.email}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
      />
      {formik.touched.email && formik.errors.email && (
        <span>{formik.errors.email}</span>
      )}
      
      <button type="submit">Submit</button>
    </form>
  )
}
```

---

## Advanced Patterns

### Dynamic Fields

```jsx
function DynamicForm() {
  const [fields, setFields] = useState([''])
  
  const addField = () => {
    setFields([...fields, ''])
  }
  
  const removeField = (index) => {
    setFields(fields.filter((_, i) => i !== index))
  }
  
  const updateField = (index, value) => {
    const newFields = [...fields]
    newFields[index] = value
    setFields(newFields)
  }
  
  return (
    <form>
      {fields.map((field, index) => (
        <div key={index}>
          <input
            value={field}
            onChange={(e) => updateField(index, e.target.value)}
          />
          <button type="button" onClick={() => removeField(index)}>
            Remove
          </button>
        </div>
      ))}
      <button type="button" onClick={addField}>Add Field</button>
    </form>
  )
}
```

### Multi-step Form

```jsx
function MultiStepForm() {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    address: ''
  })
  
  const nextStep = () => setStep(step + 1)
  const prevStep = () => setStep(step - 1)
  
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }
  
  switch (step) {
    case 1:
      return (
        <div>
          <h2>Step 1: Personal Info</h2>
          <input
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
          <button onClick={nextStep}>Next</button>
        </div>
      )
    case 2:
      return (
        <div>
          <h2>Step 2: Contact</h2>
          <input
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
          <button onClick={prevStep}>Back</button>
          <button onClick={nextStep}>Next</button>
        </div>
      )
    case 3:
      return (
        <div>
          <h2>Step 3: Address</h2>
          <input
            name="address"
            value={formData.address}
            onChange={handleChange}
          />
          <button onClick={prevStep}>Back</button>
          <button type="submit">Submit</button>
        </div>
      )
    default:
      return null
  }
}
```

---

## TypeScript

```tsx
interface FormData {
  name: string
  email: string
  age: number
}

function TypedForm() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    age: 0
  })
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'age' ? Number(value) : value
    }))
  }
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    console.log(formData)
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={handleChange}
      />
      <input
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
      />
      <input
        name="age"
        type="number"
        value={formData.age}
        onChange={handleChange}
      />
      <button type="submit">Submit</button>
    </form>
  )
}
```

<!--
Source references:
- https://react.dev/reference/react-dom/components/input
- https://react.dev/reference/react-dom/components/textarea
- https://react.dev/reference/react-dom/components/select
-->
