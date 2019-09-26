import Templates from '../templates.js'
import { mockListener, mockTemplate, mockContent, mockPage } from './__mocks__/templates.js'

const mockEvent = new Event('focus', { bubbles: false, cancelable: true })

const newContainer = document.createElement('div')
newContainer.id = 'newContent'
document.body.appendChild(newContainer)

beforeEach(() => {
  mockPage.container.innerHTML = ''
  mockContent.container.innerHTML = ''
  newContainer.innerHTML = ''
  expect(mockContent.container.children.length).toBe(0)
  expect(mockPage.container.children.length).toBe(0)
  expect(newContainer.children.length).toBe(0)
})

// This probably tests too many implementation details

test('new Listener()', () => {
  expect(mockListener).toBeTruthy()
  mockListener.eventFunction(mockEvent)

  expect(mockListener.elementPath).toBe('div')
  expect(mockListener.eventType).toBe('focus')
  expect(mockListener.eventFunction).toHaveBeenCalled()
})

test('new Template()', () => {
  expect(mockTemplate).toBeTruthy()
  mockTemplate.renderData()

  expect(mockTemplate.dataset).toBeTruthy()
  expect(mockTemplate.markup).toBe('<div class="mock"></div>')
  expect(mockTemplate.renderData).toHaveBeenCalled()
  expect(mockTemplate.listeners[0]).toBe(mockListener)
})

// Could this be a candidate for an integration test?
// Or at least to replace container with a non dom object
test('Template createContent()', () => {
  const newContent = mockTemplate.createContent(newContainer)

  expect(newContent).toBeTruthy()
  newContent.renderData()

  expect(newContent.dataset).toBeTruthy()
  expect(newContent.markup).toBe('<div class="mock"></div>')
  expect(newContent.renderData).toHaveBeenCalled()
  expect(newContent.listeners[0]).toBe(mockListener)
  expect(newContent.container.id).toBe('newContent')
})

test('new Content()', () => {
  expect(mockContent).toBeTruthy()
  mockContent.renderData()

  expect(mockContent.dataset).toBeTruthy()
  expect(mockContent.markup).toBe('<div class="mock"></div>')
  expect(mockContent.renderData).toHaveBeenCalled()
  expect(mockContent.listeners[0]).toBe(mockListener)
  expect(mockContent.container.id).toBe('contentContainer')
})

test('Content renderMarkup()', () => {
  mockContent.renderMarkup()
  expect(mockContent.container.children[0].className).toBe('mock')
})

test('Content renderContent()', () => {
  mockContent.renderContent()

  expect(mockContent.container.children[0].className).toBe('mock')
  expect(mockContent.renderData).toHaveBeenCalled()

  // purposely not testing the listeners here, those need to be integration
})

test('new Page()', () => {
  expect(mockPage).toBeTruthy()

  expect(mockPage.container.id).toBe('pageContainer')
  expect(mockPage.path).toBe('mock')
  expect(mockPage.markup).toBe('<div id="sampleContent"></div>')
  expect(mockPage.templateMap.sampleContent).toBe(mockTemplate)
  expect(mockPage.contentMap).toEqual({})
})

// Using window pathname expectations here might be better for integration tests
test('Page render()', () => {
  mockPage.render()

  expect(mockPage.container.children[0].id).toBe('sampleContent')
  expect(mockPage.container.children[0].children[0].className).toBe('mock')
  expect(mockPage.contentMap.sampleContent).toBeInstanceOf(Templates.Content)
  expect(mockPage.contentMap.sampleContent.container).toBeInstanceOf(HTMLDivElement)

  expect(window.location.pathname).toBe('/app/mock')
})
