
const content = ({ markup, listeners, dataset, renderData }, container) => {
  const render = () => {
    clear()
    container.innerHTML = markup

    // need to handle this better async
    return renderData(container)
      .then(result => {
        if (listeners.length) {
          listeners.forEach(listener => {
            listener.render(container)
          })
        }
      })
      .catch(error => {
        console.log(error.message)
      })
  }

  const clear = () => {
    if (container && container.children && container.children.length > 0) {
      Array.from(container.children).forEach(child => container.removeChild(child))
    }
    // delete the content??
  }

  const attrs = () => {
    return {
      markup: markup,
      listeners: listeners,
      dataset: dataset,
      renderData: renderData,
      container: container
    }
  }

  return {
    render: render,
    clear: clear,
    attrs: attrs
  }
}

const page = (path, markup, templateMap) => {
  let contentMap = {}
  let container

  const render = (newContainer) => {
    clear()
    container = newContainer
    container.innerHTML = markup

    const contentPromises = []
    for (const template in templateMap) {
      const newContent = content(templateMap[template], document.querySelector(`#${template}`))
      contentMap[template] = newContent

      contentPromises.push(newContent.render())
    }

    history.pushState(null, '', `/app/${path}`)

    return Promise.all(contentPromises)
  }

  const clear = () => {
    if (container && container.children && container.children.length > 0) {
      Array.from(container.children).forEach(child => container.removeChild(child))
    }
    container = null
    // delete the page??

    for (const pageContent in contentMap) {
      contentMap[pageContent].clear()
    }
    contentMap = {}
    // delete the content??
  }

  const attrs = () => {
    return {
      path: path,
      markup: markup,
      templateMap: templateMap,
      contentMap: contentMap,
      container: container
    }
  }

  return {
    render: render,
    clear: clear,
    attrs: attrs
  }
}

const listener = (elementPath, eventType, eventFunction) => {
  // maybe remove elementPath and just send in element
  let container
  let element

  const render = (newContainer) => {
    container = newContainer
    element = document.querySelector(`#${container.id} ${elementPath}`)
    element.addEventListener(eventType, eventFunction)
  }

  const clear = () => {
    container = null
    if (element) {
      element.removeEventListener(eventType, eventFunction)
    }
    element = null
  }

  const attrs = () => {
    return {
      elementPath: elementPath,
      eventType: eventType,
      eventFunction: eventFunction,
      container: container,
      element: element
    }
  }

  return {
    render: render,
    clear: clear,
    attrs: attrs
  }
}

export default { content, page, listener }
