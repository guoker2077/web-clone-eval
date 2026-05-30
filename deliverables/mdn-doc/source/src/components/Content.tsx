import '../styles/content.css'

export default function Content() {
  return (
    <>
      <h1 className="page-title">
        <code>&lt;a&gt;</code>: The Anchor element
      </h1>

      <div className="baseline-box">
        <span className="baseline-check">✓</span>
        <span className="baseline-text">
          <strong>Baseline</strong> Widely available
        </span>
      </div>

      <p>
        The <code>&lt;a&gt;</code>{' '}
        <a href="/en-US/docs/Web/HTML">HTML</a> element (or <em>anchor</em>{' '}
        element), with{' '}
        <a href="/en-US/docs/Web/HTML/Reference/Elements/a#href">its <code>href</code> attribute</a>,
        creates a hyperlink to web pages, files, email addresses, locations in
        the same page, or anything else a URL can address.
      </p>

      <p>
        Content within each <code>&lt;a&gt;</code> <em>should</em> indicate the
        link's destination. If the <code>href</code> attribute is present,
        pressing the enter key while focused on the <code>&lt;a&gt;</code> element
        will activate it.
      </p>

      <section id="try_it" className="content-section">
        <h2 className="section-heading">Try it</h2>
        <div className="demo-box">
          <div className="demo-tabs">
            <button type="button" className="demo-tab active">
              HTML
            </button>
            <button type="button" className="demo-tab">
              CSS
            </button>
            <button type="button" className="demo-reset">
              Reset
            </button>
          </div>
          <div className="demo-body">
            <pre className="demo-code">
{`<p>You can reach Michael at:</p>

<ul>
  <li><a href="https://example.com">Website</a></li>
  <li><a href="mailto:m.bluth@example.com">Email</a></li>
  <li><a href="tel:+123456789">Phone</a></li>
</ul>`}
            </pre>
            <div className="demo-output">
              <p>You can reach Michael at:</p>
              <ul>
                <li>
                  <a href="https://example.com">Website</a>
                </li>
                <li>
                  <a href="mailto:m.bluth@example.com">Email</a>
                </li>
                <li>
                  <a href="tel:+123456789">Phone</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section id="attributes" className="content-section">
        <h2 className="section-heading">Attributes</h2>
        <p>
          This element's attributes include the{' '}
          <a
            href="/en-US/docs/Web/HTML/Reference/Global_attributes"
            data-testid="content-global-attributes"
          >
            global attributes
          </a>
          .
        </p>

        <dl className="attr-list">
          <dt id="attributionsrc">
            <a href="#attributionsrc">
              <code>attributionsrc</code>
            </a>{' '}
            <span className="badge experimental">Experimental</span>
          </dt>
          <dd>
            Specifies that you want the browser to send an{' '}
            <code>Attribution-Reporting-Eligible</code> header. On the
            server-side this is used to trigger sending an{' '}
            <code>Attribution-Reporting-Register-Source</code> header in the
            response, to register a navigation-based attribution source.
          </dd>

          <dt id="download">
            <a href="#download" data-testid="content-attr-download">
              <code>download</code>
            </a>
          </dt>
          <dd>
            Causes the browser to treat the linked URL as a download. Can be used
            with or without a <code>filename</code> value.
          </dd>

          <dt id="href">
            <a href="#href">
              <code>href</code>
            </a>
          </dt>
          <dd>
            The URL that the hyperlink points to. Links are not restricted to
            HTTP-based URLs — they can use any URL scheme supported by browsers.
          </dd>

          <dt id="hreflang">
            <a href="#hreflang" data-testid="content-attr-hreflang">
              <code>hreflang</code>
            </a>
          </dt>
          <dd>
            Hints at the human language of the linked URL. No built-in
            functionality. Allowed values are the same as the{' '}
            <code>lang</code> global attribute.
          </dd>

          <dt id="ping">
            <a href="#ping">
              <code>ping</code>
            </a>
          </dt>
          <dd>
            A space-separated list of URLs. When the link is followed, the
            browser will send <code>POST</code> requests with the body{' '}
            <code>PING</code> to the URLs. Typically for tracking.
          </dd>

          <dt id="referrerpolicy">
            <a href="#referrerpolicy">
              <code>referrerpolicy</code>
            </a>
          </dt>
          <dd>How much of the referrer to send when following the link.</dd>

          <dt id="rel">
            <a href="#rel">
              <code>rel</code>
            </a>
          </dt>
          <dd>
            The relationship of the linked URL as space-separated link types.
          </dd>

          <dt id="target">
            <a href="#target">
              <code>target</code>
            </a>
          </dt>
          <dd>
            Where to display the linked URL, as the name for a browsing context
            (a tab, window, or <code>&lt;iframe&gt;</code>).
          </dd>
        </dl>
      </section>

      <section id="accessibility" className="content-section">
        <h2 className="section-heading">Accessibility</h2>
        <p>
          Strong link text benefits all users, especially those using screen
          readers. Avoid generic text like "click here" and describe the link's
          destination instead.
        </p>
      </section>

      <section id="examples" className="content-section">
        <h2 className="section-heading">Examples</h2>
        <h3 className="sub-heading">Linking to an absolute URL</h3>
        <pre className="block-code">
{`<a href="https://www.mozilla.com">Mozilla</a>`}
        </pre>
        <h3 className="sub-heading">Linking to relative URLs</h3>
        <pre className="block-code">
{`<a href="//example.com">Scheme-relative URL</a>
<a href="/en-US/docs/Web/HTML">Origin-relative URL</a>
<a href="p">Directory-relative URL</a>`}
        </pre>
      </section>

      <section id="security_and_privacy" className="content-section">
        <h2 className="section-heading">Security and privacy</h2>
        <p>
          <code>&lt;a&gt;</code> elements can have consequences for users'
          security and privacy. Use <code>rel="noopener"</code> or{' '}
          <code>rel="noreferrer"</code> when linking to untrusted content.
        </p>
      </section>

      <section id="technical_summary" className="content-section">
        <h2 className="section-heading">Technical summary</h2>
        <table className="summary-table">
          <tbody>
            <tr>
              <th>Content categories</th>
              <td>
                Flow content, phrasing content, interactive content, palpable
                content.
              </td>
            </tr>
            <tr>
              <th>Permitted content</th>
              <td>Transparent, containing either flow or phrasing content.</td>
            </tr>
            <tr>
              <th>Tag omission</th>
              <td>None, both the starting and ending tag are mandatory.</td>
            </tr>
            <tr>
              <th>DOM interface</th>
              <td>
                <code>HTMLAnchorElement</code>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <section id="specifications" className="content-section">
        <h2 className="section-heading">Specifications</h2>
        <table className="summary-table">
          <thead>
            <tr>
              <th>Specification</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>HTML Standard # the-a-element</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section id="browser_compatibility" className="content-section">
        <h2 className="section-heading">Browser compatibility</h2>
        <p>
          The <code>&lt;a&gt;</code> element is supported in all major browsers,
          including Chrome, Edge, Firefox, Safari, and Opera.
        </p>
      </section>

      <section id="see_also" className="content-section">
        <h2 className="section-heading">See also</h2>
        <ul>
          <li>
            <a href="/en-US/docs/Web/CSS">
              Other elements that are somehow related to the <code>&lt;a&gt;</code>{' '}
              element
            </a>
          </li>
          <li>
            <a href="/en-US/docs/Web/HTML/Reference/Elements/link">
              The <code>&lt;link&gt;</code> element
            </a>
          </li>
        </ul>
      </section>
    </>
  )
}
