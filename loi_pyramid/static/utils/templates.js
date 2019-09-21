class Template {
    constructor(dataset, markup, renderData, listeners) {
        this.dataset = dataset;
        this.markup = markup;
        this.renderData = renderData;
        this.listeners = listeners;
    }

    //spread operator? ...
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
        this.renderData();
        this.addListeners();
    }
}

class Page {
    constructor(container, path, markup, templateMap) {
        this.container = container;
        this.path = path;
        this.markup = markup;
        this.templateMap = templateMap;
    }

    render() {
        if (this.container && this.container.children.length > 0) {
            Array.from(this.container.children).forEach( child => this.container.removeChild(child))
        }

        this.container.innerHTML = this.markup;

        for (let template in this.templateMap) {
            let content = this.templateMap[template].createContent(document.querySelector(`#${template}`));
            content.renderContent()
        }

        history.pushState(null, '', `/app/${this.path}`);
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