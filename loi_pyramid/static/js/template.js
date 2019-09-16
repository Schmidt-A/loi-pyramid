class Content {
	constructor(beforeRender, markup, afterRender) {
		this.beforeRender = beforeRender;
		this.markup = markup;
		this.afterRender = afterRender;
		this.container;
	}

	render(container) {
		this.container = container;
	  container.innerHTML = this.markup;
	}
}

class Page extends Content {
	constructor(path, beforeRender, markup, templateMap, afterRender) {
		super(beforeRender, markup, afterRender);
		this.path = path;
		this.templateMap = templateMap;
	}

	render(container) {
		if (container && container.children.length > 0) {
			Array.from(container.children).forEach( child => container.removeChild(child))
		}

		super.render(container);

		for (let template in this.templateMap) {
			try {
        this.templateMap[template].render(document.querySelector(`#${template}`));
			} catch (error) {
				console.error(`Could not draw template ${template} because: ${error}`);
			}
    }

		history.pushState(null, '', `/app/${this.path}`);
	}
}

export default { Content, Page };