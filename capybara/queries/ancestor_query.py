from xpath import dsl as x
from xpath.renderer import to_xpath

from capybara.queries.selector_query import SelectorQuery
from capybara.result import Result


class AncestorQuery(SelectorQuery):
    def resolve_for(self, node, exact=None):
        setattr(self, "_resolved_node", node)

        @node.synchronize()
        def resolve():
            match_result = super(type(self), self).resolve_for(
                node.session.current_scope, exact=exact)

            return node.find_all(
                "xpath", to_xpath(x.ancestor()), filter=lambda el: el in match_result)

        return resolve()

    @property
    def description(self):
        description = super(type(self), self).description

        resolved_node = getattr(self, "_resolved_node", None)
        child_query = getattr(resolved_node, "query", None)
        if child_query:
            description += " that is an ancestor of {}".format(child_query.description)

        return description
