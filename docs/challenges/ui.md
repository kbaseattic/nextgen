# KBase User Interface Major Challenges and Obstacles

Compiled March, 2015

(To be honest, I'm not sure how detailed, or what counts as a "major" challenge, but here are some fairly large issues to deal with -- Bill)

### Repository management
We currently have two (three?) repos for user interface code
- __ui-common__ - contains most widget code, external dependencies, as well as the "functional site" - dashboard and landing pages
- __narrative__ - contains the code for the NI extensions to IPython, and all front end code for the NI. This includes a number of NI engine widgets, and numerous other widgets that are (ugh) copied from ui-common
- __workspace-browser__ (tentatively) - contains the Workspace Browser as a separately deployable application, factored out of the code that lives in ui-common

This is a little bit of a shambles with code copying and maybe a little too much overlap of use in certain places. I believe that ui-common should only contain modular pieces of code that will be shared among multiple repos - namely the widgets, KBase client API, and external dependencies, and everything else should use ui-common as a subrepo. This implies some work:

1. Factor the Functional Site out of ui-common into its own repo
2. Make the remaining ui-common code deployable in such a way that it can either:
  - Be fetched from a CDN (cdn.kbase.us, maybe?)
  - Be included as a subrepo (which might be cleaner, but also implies some work to keep up the subrepos when widget code changes, or only use head of a certain branch of ui-common as the subrepo)
3. Refactor both the functional site and narrative to use those subrepos for their widgets

### Search

### Workspace Browser
There's still the lingering question of how KBase wants to have users interact with their workspaces outside of the NI, and how the Workspace Browser should be designed to support that interaction.

### Landing Pages

### Dashboard

### Narrative
Lots of things here, some critical, some major, some not so much.
- Update to IPython 3.0
  - Ideally, we should reorganize all of the Narrative code to make use of how IPython does things so we can make extensions. The recent (and incomplete) migration to using an asynchronous loader (require.js) will help with that.
  - Fernando's team is starting to use Phosphor.js for developing the UX components. We should interact with them some more and follow suit
- Update the provisioning code to be done through Jupyterhub
  - Docker Swarm is another option
  - Either way, we need some better Docker container management with more options, and ideally an administration interface
- Load balancing and testing
  - If we suddenly have a swarm of a few hundred users show up, what happens?
  - We need a way to load balance - send users/containers to a parallel machine(s) to maintain load
  - We also need to more tightly control how much juice each container users. It's currently not an issue, unless some power user decides they want to, say, fork 20 processes to calculate bitcoins, or download an entire set of reads into their kernel and run their own assembly algorithm on it.
- Adjust logging
  - Less "adjust" and more "use it better." Log statements should be triggered by the method_call and app_call statements so they can be more tightly controlled, rather than by the encapsulating Service.py logging.
  - This applies to the UI as well. Error logging should be better managed, and include signin and signout events. Other significant events that are triggered in the UI - starting a job, finishing a job, deleting a job, seeing an error returned, etc. - should also be captured.
- Stop the abuse of Markdown cells
  - KBase cells (app, method, viewer) should all be refactored to make use of code cells. In the long run, this will more easily allow users to toggle over into "coding" mode, and maybe back again.
  - We can also make use of IPython's own widgets this way.
- Workspace object caching
  - Currently, the Javascript widgets all download workspace objects before processing them for visualization. Some of them pull in massive objects. This can be done multiple times, if multiple viewers are open. We can address this by doing some combination of:
    - Use IPython as a middle-end cache, and have the "widgets" make kernel calls to get data. Can even move some of the processing/pre-render code to the back end
    - Use another type of server like node.js to do the same. This has the benefit of being transparent to the Javascript developer, and whole pieces of the DOM can be rendered and just returned to the browser.
    - Client-side caching - not recommended if we can help it, but might help with some rendering steps
- __TESTING__
  - 'nuff said.
  - Okay, maybe not enough said. This JIRA ticket - https://atlassian.kbase.us/browse/NAR-131 - has a few suggestions for testing that I stand by for the general unit tests. Neal also suggested using Protractor - http://angular.github.io/protractor/#/ - for end to end testing, though that's only specific to AngularJS.
