import { LightningElement, api, track } from 'lwc';
import { NavigationMixin as navigationMixin } from 'lightning/navigation';

const DEFAULT_EXPAND_DEPTH = 2,
    DEPTH_START = 0,
    NavBase = navigationMixin(LightningElement),
    ONE = 1,
    STATUS_CLASS_MAP = {
        'Backfill': 'status-badge status-badge--backfill',
        'In-Seat': 'status-badge status-badge--inseat',
        'Net New': 'status-badge status-badge--netnew'
    },
    ZERO = 0;

export default class OrgNode extends NavBase {
    @api person;
    @api children = [];
    @api depth = DEPTH_START;
    @track isExpanded = false;

    connectedCallback() {
        this.isExpanded = this.depth < DEFAULT_EXPAND_DEPTH;
    }

    get hasChildren() {
        return this.children && this.children.length > ZERO;
    }

    get chevronIcon() {
        if (this.isExpanded) { return 'utility:chevrondown'; }
        return 'utility:chevronright';
    }

    get nextDepth() {
        return this.depth + ONE;
    }

    get nodeClass() {
        return `org-node org-node--depth-${this.depth}`;
    }

    get statusBadgeClass() {
        return STATUS_CLASS_MAP[this.person.Status__c] || 'status-badge';
    }

    get subtreeTotals() {
        return this.calcTotals(this.children);
    }

    static countSingleNode(acc, node) {
        acc.total += ONE;
        if (node.person.Status__c === 'In-Seat') { acc.inSeat += ONE; }
        else if (node.person.Status__c === 'Backfill') { acc.backfill += ONE; }
        else if (node.person.Status__c === 'Net New') { acc.netNew += ONE; }
    }

    calcTotals(nodes) {
        const acc = { backfill: ZERO, inSeat: ZERO, netNew: ZERO, total: ZERO };
        nodes.forEach(node => {
            OrgNode.countSingleNode(acc, node);
            if (node.children && node.children.length > ZERO) {
                const sub = this.calcTotals(node.children);
                acc.backfill += sub.backfill;
                acc.inSeat += sub.inSeat;
                acc.netNew += sub.netNew;
                acc.total += sub.total;
            }
        });
        return acc;
    }

    toggleExpand(event) {
        event.stopPropagation();
        if (this.hasChildren) {
            this.isExpanded = !this.isExpanded;
        }
    }

    handlePersonClick(event) {
        event.stopPropagation();
        this[navigationMixin.Navigate]({
            attributes: {
                actionName: 'view',
                recordId: event.target.dataset.id
            },
            type: 'standard__recordPage'
        });
    }

    bubblePersonClick(event) {
        this.dispatchEvent(new CustomEvent('personclick', {
            bubbles: true,
            composed: true,
            detail: event.detail
        }));
    }
}
