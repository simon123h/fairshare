import { createI18n } from 'vue-i18n';
import en from '../locales/en.json';
import de from '../locales/de.json';
import fr from '../locales/fr.json';
import lt from '../locales/lt.json';
import ja from '../locales/ja.json';
import zh from '../locales/zh.json';

export const SUPPORTED_LOCALES = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'lt', name: 'Lietuvių', flag: '🇱🇹' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' },
  { code: 'zh', name: '中文', flag: '🇨🇳' }
];

const messages = { en, de, fr, lt, ja, zh };

// Detect system/browser language and find best match
const detectLanguage = (): string => {
  const saved = localStorage.getItem('fairshare-locale');
  if (saved && messages[saved as keyof typeof messages]) {
    return saved;
  }
  const browserLang = navigator.language.split('-')[0];
  if (messages[browserLang as keyof typeof messages]) {
    return browserLang;
  }
  return 'en';
};

const i18n = createI18n({
  legacy: false,
  locale: detectLanguage(),
  fallbackLocale: 'en',
  messages
});

export default i18n;
