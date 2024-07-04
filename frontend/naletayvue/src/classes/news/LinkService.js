class LinkService {
    constructor() {
        this.links = [];
        this.news = [];
    }

    deleteAllNews() {
        this.news = [];
    }

    deleteAllLinks() {
        this.links = [];
    }
    
    // NEWS Новости
    addNews(title, content, date, image, buttonText, buttonLink) {
        const id = this.news.length + 1;
        this.news.push({ id, title, content, date, image, buttonText, buttonLink });
    }

    getAllNews() {
        return this.news;
    }

    // POSTS посты (любые)
    addPost(title, content, date, image, buttonText, buttonLink) {
        const id = this.links.length + 1;
        this.links.push({ id, title, content, date, image, buttonText, buttonLink });
    }

    getAllPosts() {
        return this.links;
    }
}

export const linkService = new LinkService();
