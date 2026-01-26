// SICryption.js
class SICryption {
    constructor(masterKey = "Roy_SIC_Corp_2026") {
        this.key = this.hashSha256(this.hashSha512(masterKey) + "SIC_CORE_V5");
        this.header = "SIC|VAULT|V5.3.2|";
    }

    hashSha512(str) {
        return crypto.subtle.digest("SHA-512", new TextEncoder().encode(str))
            .then(buf => Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join(''));
    }

    hashSha256(str) {
        return crypto.subtle.digest("SHA-256", new TextEncoder().encode(str))
            .then(buf => Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join(''));
    }

    async encrypt(data) {
        if (!data) return "";
        const salt = Date.now().toString().slice(-24);
        const workingKey = await this.hashSha256(this.key + salt);
        let encrypted = "";
        for (let i = 0; i < data.length; i++) {
            const offset = (data.charCodeAt(i) + workingKey.charCodeAt(i % workingKey.length) + i) % 1114112;
            encrypted += String.fromCharCode(offset);
        }
        const combined = salt + encrypted;
        return this.header + btoa(combined);
    }

    async decrypt(encryptedData) {
        if (!encryptedData || !encryptedData.startsWith(this.header)) return encryptedData;
        const cleanData = atob(encryptedData.replace(this.header, ""));
        const salt = cleanData.slice(0, 24);
        const content = cleanData.slice(24);
        const workingKey = await this.hashSha256(this.key + salt);
        let decrypted = "";
        for (let i = 0; i < content.length; i++) {
            const original = (content.charCodeAt(i) - workingKey.charCodeAt(i % workingKey.length) - i) % 1114112;
            decrypted += String.fromCharCode(original);
        }
        return decrypted;
    }
}
