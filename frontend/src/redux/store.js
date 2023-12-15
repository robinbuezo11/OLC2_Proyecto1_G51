import { configureStore } from '@reduxjs/toolkit';
import appStateSlice from './features/appStateSlice';

export const store = configureStore({
    reducer: {
        appState: appStateSlice
    }
});
