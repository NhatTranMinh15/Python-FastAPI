import { StrictMode } from 'react';
import App from './App.tsx';
import './index.css';
import '../public/css/button.css';
import '../public/css/color.css';

import { createRoot } from 'react-dom/client';
import { Flowbite } from 'flowbite-react';


createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <Flowbite>
            <App />
        </Flowbite>
    </StrictMode>,
)
