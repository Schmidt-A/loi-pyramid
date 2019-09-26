class Template {
    constructor(dataset, markup, renderData, listeners) {
        this.dataset = dataset;
        this.markup = markup;
        this.renderData = renderData;
        this.listeners = listeners;
    }

    createContent(container) {
        return new Content(this.dataset, this.markup, this.renderData, this.listeners, container)
    }
}

class Content extends Template {
    constructor(dataset, markup, renderData, listeners, container) {
        super(dataset, markup, renderData, listeners);
        this.container = container;
    }

    renderMarkup() {
        this.container.innerHTML = this.markup;
    }

    addListeners() {
        this.listeners.forEach( listener => {
            let element = document.querySelector(`#${this.container.id} ${listener.elementPath}`);
            element.addEventListener(listener.eventType, listener.eventFunction);
        })
    }

    renderContent() {
        this.renderMarkup();
        //need to handle this better async
        return this.renderData().then(this.addListeners());
    }
}

class Page {
    constructor(path, markup, templateMap, container) {
        this.path = path;
        this.markup = markup;
        this.templateMap = templateMap;
        this.container = container;
        this.contentMap = {};
    }

    render() {
        this.contentMap = {};

        if (this.container && this.container.children.length > 0) {
            Array.from(this.container.children).forEach( child => this.container.removeChild(child))
        }

        this.container.innerHTML = this.markup;

        let contentPromises = [];
        for (let template in this.templateMap) {
            let content = this.templateMap[template].createContent(document.querySelector(`#${template}`));
            this.contentMap[template] = content;

            contentPromises.push(content.renderContent());
        }

        history.pushState(null, '', `/app/${this.path}`);

        return Promise.all(contentPromises);
    }
}

class Listener {
    constructor(elementPath, eventType, eventFunction) {
        this.elementPath = elementPath;
        this.eventType = eventType;
        this.eventFunction = eventFunction;
    }
}

export default { Content, Page, Template, Listener };